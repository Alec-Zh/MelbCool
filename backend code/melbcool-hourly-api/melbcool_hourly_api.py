import json
import boto3
import os
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-southeast-2'))
table = dynamodb.Table('HourlyForecast')

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def lambda_handler(event, context):
    print("EVENT:", event)

    # CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": HEADERS, "body": ""}

    path = event.get("rawPath") or event.get("path", "")
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method", "GET")

    # GET /hourly/{suburb_id}
    if method == "GET" and path.startswith("/hourly/"):
        suburb_id_str = path.split("/")[-1]
        if not suburb_id_str.isdigit():
            return {
                "statusCode": 400,
                "headers": HEADERS,
                "body": json.dumps({"error": "Invalid suburb_id"})
            }

        suburb_id = int(suburb_id_str)
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

        try:
            response = table.get_item(Key={
                'suburb_id': suburb_id,
                'date': today,
            })
        except Exception as e:
            print(f"DynamoDB error: {e}")
            return {
                "statusCode": 500,
                "headers": HEADERS,
                "body": json.dumps({"error": "Failed to read forecast data"})
            }

        item = response.get('Item')
        if not item:
            return {
                "statusCode": 404,
                "headers": HEADERS,
                "body": json.dumps({"error": "No forecast data for this suburb today"})
            }

        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({
                "suburb_id": suburb_id,
                "date": item["date"],
                "hourly_apparent_temperature": json.loads(item["hourly_apparent_temperature"]),
                "updated_at": item["updated_at"],
            })
        }

    return {
        "statusCode": 404,
        "headers": HEADERS,
        "body": json.dumps({"error": "Not found"})
    }
