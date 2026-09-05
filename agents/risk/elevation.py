import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENTOPOGRAPHY_API_KEY")

def get_elevation(latitude,longitude):
    """Get the elevation of the location"""
    
    url = "https://portal.opentopography.org/API/v1/elevation"
    params={
         "latitude":latitude,
         "longitude":longitude,
         "dataset": "COP30",
         "output_format":"json",
         "API_Key": API_KEY
     }
    
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return data["Elevation"]

if __name__ == "__main__":
    from agents.config.regions import REGIONS

    for region in REGIONS:
        if region["enabled"]:
            result = get_elevation(
                region["latitude"],
                region["longitude"]
            )

            print(region["name"], "→", result, "meters")