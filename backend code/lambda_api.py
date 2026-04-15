import json
import pymysql
import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": 3306,
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": "heatmap",
    "charset": "utf8mb4",
}

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def get_all_suburbs(cursor):
    cursor.execute("""
        SELECT 
            s.suburb_id,
            s.suburb_name,
            s.latitude,
            s.longitude,
            h.temperature,
            h.heat_level,
            h.timestamp AS updated_at,
            v.vegetation_index AS tree_canopy_percent,
            p.elderly_population,
            p.total_population,
            r.risk_level,
            r.heat_score,
            r.vulnerability_score
        FROM Suburb s
        LEFT JOIN Heat_Data h ON s.suburb_id = h.suburb_id
        LEFT JOIN Vegetation_Data v ON s.suburb_id = v.suburb_id
        LEFT JOIN Population_Data p ON s.suburb_id = p.suburb_id
        LEFT JOIN Risk_Assessment r ON s.suburb_id = r.suburb_id
        ORDER BY s.suburb_name
    """)
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in rows]

def get_suburb_by_id(cursor, suburb_id):
    cursor.execute("""
        SELECT 
            s.suburb_id,
            s.suburb_name,
            s.latitude,
            s.longitude,
            h.temperature,
            h.heat_level,
            h.timestamp AS updated_at,
            v.vegetation_index AS tree_canopy_percent,
            p.elderly_population,
            p.total_population,
            r.risk_level,
            r.heat_score,
            r.vulnerability_score
        FROM Suburb s
        LEFT JOIN Heat_Data h ON s.suburb_id = h.suburb_id
        LEFT JOIN Vegetation_Data v ON s.suburb_id = v.suburb_id
        LEFT JOIN Population_Data p ON s.suburb_id = p.suburb_id
        LEFT JOIN Risk_Assessment r ON s.suburb_id = r.suburb_id
        WHERE s.suburb_id = %s
    """, (suburb_id,))
    row = cursor.fetchone()
    if not row:
        return None
    cols = [d[0] for d in cursor.description]
    return dict(zip(cols, row))

def serialize(obj):
    import decimal
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    """Handle datetime serialization"""
    import datetime
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, datetime.timedelta):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def lambda_handler(event, context):
    print("EVENT:", event)
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": HEADERS, "body": ""}

    path = event.get("rawPath") or event.get("path", "")
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method", "GET")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # GET /suburbs
        if method == "GET" and path == "/suburbs":
            data = get_all_suburbs(cursor)
            return {
                "statusCode": 200,
                "headers": HEADERS,
                "body": json.dumps(data, default=serialize)
            }

        # GET /suburbs/{id}
        elif method == "GET" and path.startswith("/suburbs/"):
            suburb_id = path.split("/")[-1]
            if not suburb_id.isdigit():
                return {"statusCode": 400, "headers": HEADERS, "body": json.dumps({"error": "Invalid suburb ID"})}
            data = get_suburb_by_id(cursor, int(suburb_id))
            if not data:
                return {"statusCode": 404, "headers": HEADERS, "body": json.dumps({"error": "Suburb not found"})}
            return {
                "statusCode": 200,
                "headers": HEADERS,
                "body": json.dumps(data, default=serialize)
            }

        else:
            return {"statusCode": 404, "headers": HEADERS, "body": json.dumps({"error": "Not found"})}

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": "Internal server error"})
        }
    finally:
        cursor.close()
        conn.close()