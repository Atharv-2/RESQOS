import requests
from agents.config.regions import REGIONS

def get_weather(latitude,longitude):
    """Get the current weather of the specified location usingthe OpenMeteo API."""
    url="https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,precipitation_probability,temperature_2m",
        "forecast_days": 1
    }
    
    response=requests.get(url,params=params,timeout=10)
    
    response.raise_for_status()
    
    data=response.json()
    
    return data["hourly"]


def summarize_weather(weather_data):
    precipitation = weather_data["precipitation"]
    rain_probability = weather_data["precipitation_probability"]

    total_rainfall = sum(precipitation)
    max_hourly_rainfall = max(precipitation)
    max_rain_probability = max(rain_probability)

    return {
        "total_rainfall": round(total_rainfall, 2),
        "max_hourly_rainfall": max_hourly_rainfall,
        "max_rain_probability": max_rain_probability
    }
    
if __name__ == "__main__":
    region = REGIONS[4]

    name = region["name"]
    latitude = region["latitude"]
    longitude = region["longitude"]

    weather = get_weather(latitude, longitude)
    summary = summarize_weather(weather)

    print("Region:", name)
    print("Weather:", summary)
    
    