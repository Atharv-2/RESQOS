import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from agents.monitoring.weather_agent import check_rainfall_threshold
from agents.config.regions import REGIONS

from agents.tools.elevation import get_elevation
from agents.tools.river import get_nearby_waterways
from agents.tools.hospital import get_nearby_hospitals
from agents.tools.police import get_nearby_police_stations
from agents.tools.shelter import get_nearby_emergency_points




# Load environment variables
load_dotenv()


# Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


# Tools available to the agent
tools = [
    get_elevation,
    get_nearby_waterways,
    get_nearby_hospitals,
    get_nearby_police_stations,
    get_nearby_emergency_points
]


# Agent instructions
system_prompt = """
You are the RESQOS Risk Assessment Agent for Uttarakhand.

Your job is to assess heavy-rainfall situations and determine whether
additional geographic information is useful for understanding the
situation.

You receive:
- Region
- Latitude
- Longitude
- Forecast rainfall
- Rainfall threshold
- Threshold status calculated by the application

You have access to two tools:

1. get_elevation
   Returns the elevation of the affected location.

2. get_nearby_waterways
   Returns mapped rivers and streams near the affected location.

Use your reasoning to decide whether these tools are useful for the
current situation.

If the rainfall is below the configured threshold, consider whether
additional geographic analysis is actually necessary. In a normal
situation, provide practical preparedness guidelines and avoid
unnecessary tool calls.

If the rainfall threshold is breached, gather relevant geographic
information using the available tools before making your assessment.

Use tool results as evidence for your assessment.

Never invent elevation, waterways, distances, historical events,
soil conditions, flood probabilities, or other geographic facts.

When geographic information is unavailable, clearly state that it is
unavailable.

Your final response should contain:

- Risk Status
- Reason
- Important Geographic Factors, when relevant
- Recommended Next Steps
- Normal Preparedness Guidelines, when relevant

The threshold status provided by the application is authoritative.
"""


# Create the agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


def assess_risk(weather_result):
    """
    Send live weather information to the Risk Assessment Agent.
    """

    message = f"""
Assess the following heavy-rainfall situation:

Region: {weather_result["region"]}
Latitude: {weather_result["latitude"]}
Longitude: {weather_result["longitude"]}
Forecast rainfall: {weather_result["rainfall"]} mm
Rainfall threshold: {weather_result["threshold"]} mm
Threshold breached: {weather_result["breached"]}

Use your reasoning to determine whether additional geographic
information is necessary.

Use the available tools when they provide useful information.
"""


    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    })

    return result


if __name__ == "__main__":

    # Select the region to monitor
    region = next(
        region for region in REGIONS
        if region["name"] == "Dehradun"
    )


    # Get LIVE weather data from Open-Meteo
    print("\nFetching live weather data...\n")

    weather_result = check_rainfall_threshold(region)


    # Display weather information
    print("Region:", weather_result["region"])
    print("Forecast rainfall:", weather_result["rainfall"], "mm")
    print("Threshold:", weather_result["threshold"], "mm")
    print("Threshold breached:", weather_result["breached"])


    # Run Risk Assessment Agent
    print("\nRunning Risk Assessment Agent...\n")

    result = assess_risk(weather_result)


    # Display agent response
    print("\n--- RESQOS RISK AGENT ---\n")

    for msg in result["messages"]:

        if hasattr(msg, "content") and msg.content:
            print(msg.content)
