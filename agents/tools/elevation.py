import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

API_KEY = os.getenv("OPENTOPOGRAPHY_API_KEY")

@tool
def get_elevation(latitude: float, longitude: float) -> float:
    """Get the elevation of a location from OpenTopography."""

    url = "https://portal.opentopography.org/API/v1/elevation"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "output_format": "json",
        "API_Key": API_KEY,
        "dataset": "COP30"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return data["Elevation"]

if __name__ == "__main__":
    elevation = get_elevation.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322
    })
    print("Elevation:", elevation, "meters")