import os
import psycopg
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def get_nearby_waterways(
    latitude: float,
    longitude: float,
    radius_km: float = 10
):
    """
    Find rivers and waterways near a given latitude and longitude
    using the CWC River Network dataset.
    """

    radius_m = radius_km * 1000

    conn = psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "resqos"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

    query = """SELECT id,rivname,"UID_River",length_km,st_loc_dst,en_loc_dst,ST_Distance(geom::geography,ST_SetSRID(ST_MakePoint(%s,%s),4326)::geography) AS distance_m FROM public.cwc_river_network WHERE ST_DWithin(geom::geography,ST_SetSRID(ST_MakePoint(%s,%s),4326)::geography,%s) ORDER BY distance_m LIMIT 20;"""

    try:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    longitude,
                    latitude,
                    longitude,
                    latitude,
                    radius_m
                )
            )

            rows = cur.fetchall()

    finally:
        conn.close()

    waterways = []

    for row in rows:
        waterways.append({
            "gid": row[0],
            "river_name": row[1] if row[1] else "Unnamed",
            "river_id": row[2],
            "length_km": float(row[3]) if row[3] is not None else None,
            "start_district": row[4],
            "end_district": row[5],
            "distance_m": round(row[6], 2)
        })

    return waterways


@tool
def get_nearest_waterway_distance(
    latitude: float,
    longitude: float
):
    """
    Find the nearest mapped waterway within 10 km.
    """

    waterways = get_nearby_waterways.invoke({
        "latitude": latitude,
        "longitude": longitude,
        "radius_km": 10
    })

    if not waterways:
        return {
            "nearest_waterway": None,
            "distance_m": None,
            "distance_km": None,
            "message": "No mapped waterway found within 10 km."
        }

    nearest = waterways[0]

    return {
        "nearest_waterway": nearest["river_name"],
        "distance_m": nearest["distance_m"],
        "distance_km": round(nearest["distance_m"] / 1000, 2)
    }


if __name__ == "__main__":

    result = get_nearby_waterways.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322,
        "radius_km": 10
    })

    print("\n--- NEARBY WATERWAYS ---")

    for river in result:
        print(river)

    nearest = get_nearest_waterway_distance.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322
    })

    print("\n--- NEAREST WATERWAY ---")
    print(nearest)