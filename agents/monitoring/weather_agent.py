from agents.tools.weather import get_weather, summarize_weather
from agents.config.threshold import RAINFALL_THRESHOLD
from agents.config.regions import REGIONS


def check_rainfall_threshold(region):
    """Fetch live weather forecast and check the rainfall threshold."""

    name = region["name"]
    latitude = region["latitude"]
    longitude = region["longitude"]

    weather = get_weather(latitude, longitude)

    summary = summarize_weather(weather)

    total_rainfall = summary["total_rainfall"]

    breached = total_rainfall >= RAINFALL_THRESHOLD

    return {
        "region": name,
        "latitude": latitude,
        "longitude": longitude,
        "rainfall": total_rainfall,
        "threshold": RAINFALL_THRESHOLD,
        "breached": breached
    }


if __name__ == "__main__":

    region = next(
        region for region in REGIONS
        if region["name"] == "Dehradun"
    )

    result = check_rainfall_threshold(region)

    print("\n--- RESQOS WEATHER MONITOR ---\n")

    print("Region:", result["region"])
    print("Forecast rainfall:", result["rainfall"], "mm")
    print("Threshold:", result["threshold"], "mm")
    print("Threshold breached:", result["breached"])