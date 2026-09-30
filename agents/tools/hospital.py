import os
import psycopg
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def get_nearby_hospitals(
    latitude: float,
    longitude: float,
    radius_km: float = 10
):
    """
    Find hospitals near a given latitude and longitude.
    """

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
            gid,
            name,
            amenity,
            "addr:city",
            phone,
            ST_Distance(
                way::geography,
                ST_SetSRID(
                    ST_MakePoint(%s, %s),
                    4326
                )::geography
            ) AS distance_m
        FROM public.emergency_hospitals
        WHERE ST_DWithin(
            way::geography,
            ST_SetSRID(
                ST_MakePoint(%s, %s),
                4326
            )::geography,
            %s
        )
        ORDER BY distance_m
        LIMIT 20;
    """

    with conn:
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

    conn.close()

    hospitals = []

    for row in rows:
        hospitals.append({
            "gid": row[0],
            "name": row[1],
            "amenity": row[2],
            "city": row[3],
            "phone": row[4],
            "distance_m": round(row[5], 2)
        })

    return hospitals


if __name__ == "__main__":

    result = get_nearby_hospitals.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322,
        "radius_km": 10
    })

    print("\n--- NEARBY HOSPITALS ---")

    for hospital in result:
        print(hospital)
