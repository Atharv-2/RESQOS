import os
import psycopg
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def get_nearby_emergency_points(
    latitude: float,
    longitude: float,
    radius_km: float = 10
):
    """
    Find nearby emergency points such as shelters,
    community centres, town halls and fire stations.
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
            point_type,
            ST_Distance(
                ST_Transform(way, 4326)::geography,
                ST_SetSRID(
                    ST_MakePoint(%s, %s),
                    4326
                )::geography
            ) AS distance_m
        FROM public.emergency_points
        WHERE ST_DWithin(
            ST_Transform(way, 4326)::geography,
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

    emergency_points = []

    for row in rows:
        emergency_points.append({
            "gid": row[0],
            "name": row[1],
            "type": row[2],
            "distance_m": round(row[3], 2)
        })

    return emergency_points


if __name__ == "__main__":

    result = get_nearby_emergency_points.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322,
        "radius_km": 10
    })

    print("\n--- NEARBY EMERGENCY POINTS ---")

    for point in result:
        print(point)