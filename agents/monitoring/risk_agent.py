import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agents.monitoring.weather_agent import check_rainfall_threshold
from agents.config.regions import REGIONS

from agents.tools.elevation import get_elevation
from agents.tools.river import get_nearby_waterways
from agents.tools.hospital import get_nearby_hospitals
from agents.tools.police import get_nearby_police_stations
from agents.tools.shelter import get_nearby_emergency_points


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


system_prompt = """
You are the RESQOS Risk Assessment Agent for Uttarakhand.

You operate as an agent.

Your job is to examine evidence about a monitored location and
decide what information should be collected next.

Available actions:

get_elevation
get_waterways
get_hospitals
get_police
get_emergency_points
finish

You must respond with exactly ONE action name and nothing else.

Do not provide coordinates.
Do not provide JSON.
Do not provide arguments.
Do not call tools yourself.

The application will execute the selected action using trusted
coordinates.

Decision rules:

1. If elevation has not been collected, choose get_elevation.

2. If waterways have not been collected, choose get_waterways.

3. If hospitals have not been collected, choose get_hospitals.

4. If police stations have not been collected, choose get_police.

5. If emergency points have not been collected, choose
   get_emergency_points.

6. Once sufficient evidence has been collected, choose finish.

Never invent information.
"""


def choose_action(context):
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": context
            }
        ]
    )

    action = response.content.strip().lower()

    valid_actions = {
        "get_elevation",
        "get_waterways",
        "get_hospitals",
        "get_police",
        "get_emergency_points",
        "finish"
    }

    if action in valid_actions:
        return action

    for valid_action in valid_actions:
        if valid_action in action:
            return valid_action

    raise ValueError(f"Invalid agent action: {action}")


def execute_action(action, latitude, longitude):

    if action == "get_elevation":

        result = get_elevation.invoke({
            "latitude": latitude,
            "longitude": longitude
        })

        return result

    if action == "get_waterways":

        result = get_nearby_waterways.invoke({
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": 10
        })

        return result[:5]

    if action == "get_hospitals":

        result = get_nearby_hospitals.invoke({
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": 10
        })

        return result[:5]

    if action == "get_police":

        result = get_nearby_police_stations.invoke({
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": 10
        })

        return result[:5]

    if action == "get_emergency_points":

        result = get_nearby_emergency_points.invoke({
            "latitude": latitude,
            "longitude": longitude,
            "radius_km": 10
        })

        return result[:5]

    return None


def generate_assessment(weather_result, evidence):

    prompt = f"""
Assess this RESQOS monitored location.

Region: {weather_result["region"]}
Latitude: {weather_result["latitude"]}
Longitude: {weather_result["longitude"]}
Forecast rainfall: {weather_result["rainfall"]} mm
Rainfall threshold: {weather_result["threshold"]} mm
Threshold breached: {weather_result["breached"]}

The rainfall threshold status supplied by the application is
authoritative.

Evidence collected by the RESQOS agent:

{json.dumps(evidence, indent=2, default=str)}

RISK STATUS

If Threshold breached is True:

Report:

Elevated Attention

This means the configured rainfall threshold has been breached
for the RESQOS prototype.

It does NOT mean that flooding is occurring.

If Threshold breached is False:

Report:

Normal Monitoring

EVIDENCE RULES

Only report information contained in the weather data or collected
evidence.

Do not invent:

- Flood probability
- River water levels
- Current flooding
- Evacuation distances
- Safe distances
- Shelter capacity
- Hospital capabilities
- Police capabilities
- Emergency response times
- Drainage conditions
- Soil conditions
- Runoff behaviour
- Historical flood events
- Hydrological conditions

Recommendations should be limited to evidence-supported actions.

Do not issue evacuation instructions.

FINAL RESPONSE

Use exactly these sections:

Risk Status

Reason

Important Geographic Factors

Emergency Resources

Recommended Next Steps

Limitations

Keep the assessment concise.
"""

    response = llm.invoke([
        {
            "role": "system",
            "content": "You are the final RESQOS risk assessment agent. Use only supplied evidence."
        },
        {
            "role": "user",
            "content": prompt
        }
    ])

    return response.content


def assess_risk(weather_result):

    latitude = weather_result["latitude"]
    longitude = weather_result["longitude"]

    evidence = {}

    max_steps = 6

    for step in range(max_steps):

        context = f"""
Region: {weather_result["region"]}

Latitude: {latitude}
Longitude: {longitude}

Forecast rainfall: {weather_result["rainfall"]} mm
Rainfall threshold: {weather_result["threshold"]} mm
Threshold breached: {weather_result["breached"]}

Evidence already collected:

{json.dumps(evidence, indent=2, default=str)}

Choose the next action.

Available actions:

get_elevation
get_waterways
get_hospitals
get_police
get_emergency_points
finish
"""

        action = choose_action(context)

        print(f"Agent decision {step + 1}: {action}")

        if action == "finish":
            break

        if action in evidence:
            print(f"Already collected: {action}")
            continue

        try:
            result = execute_action(
                action,
                latitude,
                longitude
            )

            evidence[action] = result

            print(f"Tool completed: {action}")

        except Exception as e:

            print(f"Tool failed: {action}")
            print(f"Error: {e}")

            evidence[action] = {
                "error": str(e)
            }

    print("\nGenerating final assessment...\n")

    return generate_assessment(
        weather_result,
        evidence
    )


if __name__ == "__main__":

    for region in REGIONS:

        if not region["enabled"]:
            continue

        print("\n" + "=" * 70)
        print(f"REGION: {region['name']}")
        print("=" * 70)

        try:

            print("\nFetching live weather data...\n")

            weather_result = check_rainfall_threshold(region)

            print(
                "Forecast rainfall:",
                weather_result["rainfall"],
                "mm"
            )

            print(
                "Threshold:",
                weather_result["threshold"],
                "mm"
            )

            print(
                "Threshold breached:",
                weather_result["breached"]
            )

            if not weather_result["breached"]:

                print("\nNormal monitoring. No risk assessment required.")
                continue

            print("\nStarting Risk Assessment Agent...\n")

            assessment = assess_risk(weather_result)

            print("\n--- RESQOS RISK AGENT ---\n")
            print(assessment)

        except Exception as e:

            print("\n!!! FAILED !!!")
            print("Region:", region["name"])
            print("Error:", e)