from agents.tools.weather_tool import get_weather, summarize_weather
from agents.config.threshold import RAINFALL_THRESHOLD


def check_rainfall_threshold(region):
    """Check whether a region's forecast rainfall exceeds the threshold."""

    name = region["name"]
    latitude = region["latitude"]
    longitude = region["longitude"]

    weather = get_weather(latitude, longitude)
    summary = summarize_weather(weather)

    total_rainfall = summary["total_rainfall"]

    breached = total_rainfall >= RAINFALL_THRESHOLD

    return {
        "region": name,
        "rainfall": total_rainfall,
        "threshold": RAINFALL_THRESHOLD,
        "breached": breached
    }
    
    
if __name__ == "__main__":
    from agents.config.regions import REGIONS

    for region in REGIONS:
        if region["enabled"]:
            result = check_rainfall_threshold(region)
            print(result)