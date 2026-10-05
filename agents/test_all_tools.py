from agents.config.regions import REGIONS
from agents.tools.elevation import get_elevation
from agents.tools.river import get_nearby_waterways
from agents.tools.hospital import get_nearby_hospitals
from agents.tools.police import get_nearby_police_stations
from agents.tools.shelter import get_nearby_emergency_points


def test_tool(name, tool, latitude, longitude, radius_km=None):
    try:
        if radius_km is None:
            result = tool.invoke({
                "latitude": latitude,
                "longitude": longitude
            })
        else:
            result = tool.invoke({
                "latitude": latitude,
                "longitude": longitude,
                "radius_km": radius_km
            })

        if isinstance(result, list):
            print(f"{name:<15}: OK ({len(result)} results)")
        else:
            print(f"{name:<15}: OK")

    except Exception as e:
        print(f"{name:<15}: FAILED")
        print(f"    Error: {e}")


def main():

    for region in REGIONS:

        if not region["enabled"]:
            continue

        name = region["name"]
        latitude = region["latitude"]
        longitude = region["longitude"]

        print("\n" + "=" * 50)
        print(name)
        print(f"Coordinates: {latitude}, {longitude}")
        print("=" * 50)

        test_tool(
            "Elevation",
            get_elevation,
            latitude,
            longitude
        )

        test_tool(
            "Waterways",
            get_nearby_waterways,
            latitude,
            longitude,
            10
        )

        test_tool(
            "Hospitals",
            get_nearby_hospitals,
            latitude,
            longitude,
            10
        )

        test_tool(
            "Police",
            get_nearby_police_stations,
            latitude,
            longitude,
            10
        )

        test_tool(
            "Emergency",
            get_nearby_emergency_points,
            latitude,
            longitude,
            10
        )


if __name__ == "__main__":
    main()