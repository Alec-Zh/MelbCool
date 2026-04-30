import json
import urllib.request
import boto3
import os
from datetime import datetime, timezone

# DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-southeast-2'))
table = dynamodb.Table('HourlyForecast')

# RDS config — reuse existing env vars to read suburb list
import pymysql

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": 3306,
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": "heatmap",
    "charset": "utf8mb4",
}

BATCH_SIZE = 50
MAX_RETRIES = 3


def fetch_hourly_batch(suburbs):
    """
    suburbs: list of (suburb_id, latitude, longitude)
    Returns: { suburb_id: [24 apparent_temperature values] }
    """
    results = {}

    for i in range(0, len(suburbs), BATCH_SIZE):
        batch = suburbs[i:i + BATCH_SIZE]
        lats = ','.join(str(round(s[1], 4)) for s in batch)
        lons = ','.join(str(round(s[2], 4)) for s in batch)
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lats}&longitude={lons}"
            f"&hourly=apparent_temperature"
            f"&timezone=Australia%2FSydney"
            f"&forecast_days=1"
        )

        for attempt in range(MAX_RETRIES):
            try:
                with urllib.request.urlopen(url, timeout=20) as resp:
                    data = json.loads(resp.read())
                    if isinstance(data, dict):
                        data = [data]
                    for j, item in enumerate(data):
                        results[batch[j][0]] = item['hourly']['apparent_temperature']
                    break
            except Exception as e:
                print(f"Batch {i // BATCH_SIZE + 1} attempt {attempt + 1} failed: {e}")
                if attempt == MAX_RETRIES - 1:
                    print(f"Skipping batch {i // BATCH_SIZE + 1} after {MAX_RETRIES} attempts")

    return results


def lambda_handler(event, context):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Read suburb list from RDS
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT suburb_id, latitude, longitude FROM Suburb")
    suburbs = cursor.fetchall()  # (suburb_id, lat, lon)
    cursor.close()
    conn.close()
    print(f"Fetching hourly forecast for {len(suburbs)} suburbs...")

    hourly_map = fetch_hourly_batch(suburbs)

    # Write to DynamoDB
    updated = 0
    with table.batch_writer() as batch:
        for suburb_id, lat, lon in suburbs:
            hourly = hourly_map.get(suburb_id)
            if hourly is None:
                continue
            batch.put_item(Item={
                'suburb_id': suburb_id,
                'date': today,
                'hourly_apparent_temperature': json.dumps(hourly),  # store as JSON string
                'updated_at': datetime.now(timezone.utc).isoformat(),
            })
            updated += 1

    print(f"Done: {updated} suburbs written to DynamoDB")
    return {'statusCode': 200, 'body': json.dumps({'updated': updated})}
