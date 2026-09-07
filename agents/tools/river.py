import os
import psycopg
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()

@tool
def get_nearby_waterways(latitude:float, longitude:float, radius_km:float=2):
    """Find nearby rivers and streams within the specified radius using PostGIS."""

    radius_m = radius_km * 1000

    conn = psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "resqos"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

    query = """
    SELECT
        osm_id,
        name,
        waterway,
        ST_Distance(
            ST_Transform(way, 4326)::geography,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
        ) AS distance_m
    FROM uttarakhand_waterways
    WHERE ST_DWithin(
        ST_Transform(way, 4326)::geography,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        %s
    )
    ORDER BY distance_m;
    """

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (longitude, latitude, longitude, latitude, radius_m)
            )
            rows = cur.fetchall()

    conn.close()

    waterways = []

    for row in rows:
        waterways.append({
            "osm_id": row[0],
            "name": row[1],
            "waterway": row[2],
            "distance_m": round(row[3], 2)
        })

    return waterways


if __name__ == "__main__":
    waterways = get_nearby_waterways.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322,
        "radius_km": 5
    })

    print("Nearby waterways:", len(waterways))

    for waterway in waterways[:5]:
        print(waterway)