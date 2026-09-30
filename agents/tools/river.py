
import os
import psycopg
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def get_nearby_waterways(
    latitude: float,
    longitude: float,
    radius_km: float = 2
):
    """
    Find rivers/waterways near a given latitude and longitude.
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
            rivname,
            uid_river,
            length_km,
            st_loc_dst,
            en_loc_dst,
            ST_Distance(
                way::geography,
                ST_SetSRID(
                    ST_MakePoint(%s, %s),
                    4326
                )::geography
            ) AS distance_m
        FROM public.uttarakhand_waterways
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

    waterways = []

    for row in rows:
        waterways.append({
            "gid": row[0],
            "river_name": row[1],
            "river_id": row[2],
            "length_km": float(row[3]) if row[3] is not None else None,
            "start_district": row[4],
            "end_district": row[5],
            "distance_m": round(row[6], 2)
        })

    return waterways

if __name__ == "__main__":
    result = get_nearby_waterways.invoke({
        "latitude": 30.3165,
        "longitude": 78.0322,
        "radius_km": 10
    })

    print("\n--- NEARBY RIVERS ---")

    for river in result:
        print(river)
