import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


system_prompt = """
You are the RESQOS Evacuation Route Agent.

Your job is to help identify the safest feasible road route
from a person's current location to an emergency shelter.

The safest route is NOT necessarily the shortest route.

Route selection must prioritize:
1. Avoiding dangerous waterways and flood-prone areas.
2. Avoiding other identified geographic hazards.
3. Keeping travel distance and travel time reasonable.

A route that passes close to a river, stream, or other waterway
should receive a higher risk score.

However, waterways must NOT automatically make a route impossible.

If every available route has waterway exposure, select the
least-risk feasible route and clearly warn that water exposure
is unavoidable.

IMPORTANT:
- Never invent roads or route information.
- Never invent distances or risk scores.
- Use actual routing and geographic data supplied by the tools.
- The deterministic route-risk calculation is authoritative.
- The LLM should explain the route decision rather than
  independently inventing the safest route.

The final response should contain:

- Recommended Route
- Distance
- Estimated Travel Time, if available
- Risk Score
- Waterway Exposure
- Reason for Selection
- Warnings, if any
"""


agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=system_prompt
)


def recommend_route(
    user_latitude,
    user_longitude,
    shelter_latitude,
    shelter_longitude
):
    """
    Generate a route recommendation from a person's
    location to an emergency shelter.

    Actual routing and geographic risk analysis will be
    connected once the road and waterway datasets are available.
    """

    message = f"""
Find the safest feasible evacuation route.

Starting location:
Latitude: {user_latitude}
Longitude: {user_longitude}

Shelter:
Latitude: {shelter_latitude}
Longitude: {shelter_longitude}

Prioritize route safety over minimum distance.

Avoid waterways and other hazardous areas where possible.
If all feasible routes have some waterway exposure,
choose the least-risk route and clearly report the limitation.
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

    result = recommend_route(
        30.3165,
        78.0322,
        30.3250,
        78.0450
    )

    print("\n--- RESQOS ROUTE AGENT ---\n")

    for msg in result["messages"]:

        if hasattr(msg, "content") and msg.content:
            print(msg.content)