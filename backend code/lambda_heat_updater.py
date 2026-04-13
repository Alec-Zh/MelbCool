import json
import urllib.request
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

def get_heat_level(temp):
    if temp >= 35:
        return 'higher'
    elif temp >= 28:
        return 'moderate'
    else:
        return 'lower'

def get_heat_score(temp):
    if temp >= 35:
        return min(round((temp - 35) * 3 + 70, 2), 100)
    elif temp >= 28:
        return round((temp - 28) * 4.3 + 40, 2)
    else:
        return max(round(temp * 1.4, 2), 0)

def fetch_temperatures_batch(suburbs):
    results = {}
    batch_size = 50
    for i in range(0, len(suburbs), batch_size):
        batch = suburbs[i:i+batch_size]
        lats = ','.join(str(round(s[2], 4)) for s in batch)
        lons = ','.join(str(round(s[3], 4)) for s in batch)
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lats}&longitude={lons}"
            f"&current=temperature_2m"
            f"&timezone=Australia%2FSydney"
        )
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read())
            if isinstance(data, dict):
                data = [data]
            for j, item in enumerate(data):
                results[batch[j][0]] = item['current']['temperature_2m']
    return results

def lambda_handler(event, context):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT suburb_id, suburb_name, latitude, longitude FROM Suburb")
    suburbs = cursor.fetchall()
    print(f"Fetching temperatures for {len(suburbs)} suburbs...")

    temp_map = fetch_temperatures_batch(suburbs)

    cursor.execute("SELECT suburb_id, vulnerability_score FROM Risk_Assessment")
    vuln_map = {row[0]: float(row[1]) for row in cursor.fetchall()}

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE Heat_Data")

    inserted = 0
    for suburb_id, suburb_name, lat, lon in suburbs:
        temp = temp_map.get(suburb_id)
        if temp is None:
            continue

        heat_level = get_heat_level(temp)
        heat_score = get_heat_score(temp)

        cursor.execute("""
            INSERT INTO Heat_Data (suburb_id, temperature, heat_level)
            VALUES (%s, %s, %s)
        """, (suburb_id, temp, heat_level))

        vuln_score = vuln_map.get(suburb_id, 50.0)
        combined = heat_score * 0.5 + vuln_score * 0.5
        if combined >= 65:
            risk_level = 'high'
        elif combined >= 40:
            risk_level = 'moderate'
        else:
            risk_level = 'low'

        cursor.execute("""
            UPDATE Risk_Assessment
            SET heat_score = %s, risk_level = %s, generated_at = NOW()
            WHERE suburb_id = %s
        """, (heat_score, risk_level, suburb_id))

        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Done: {inserted} records updated")
    return {'statusCode': 200, 'body': json.dumps({'updated': inserted})}