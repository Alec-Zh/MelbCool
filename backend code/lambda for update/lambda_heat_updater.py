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

VEG_MIN = 2.31
VEG_MAX = 43.44

def get_heat_level(apparent_temp):
    if apparent_temp >= 35:
        return 'higher'
    elif apparent_temp >= 28:
        return 'moderate'
    else:
        return 'lower'

def get_heat_score(apparent_temp, uv_index):
    if apparent_temp >= 35:
        base = min(round((apparent_temp - 35) * 3 + 70, 2), 100)
    elif apparent_temp >= 28:
        base = round((apparent_temp - 28) * 4.3 + 40, 2)
    else:
        base = max(round(apparent_temp * 1.4, 2), 0)
    uv_bonus = min(round(uv_index * 1.8, 2), 20)
    return min(base + uv_bonus, 100)

def get_shade_score(veg_index):
    # 归一化到 0-100，反转：绿化越高 = 暴露风险越低
    normalized = (veg_index - VEG_MIN) / (VEG_MAX - VEG_MIN) * 100
    return round(max(min(100 - normalized, 100), 0), 2)

def fetch_temperatures_batch(suburbs):
    results = {}
    batch_size = 50
    max_retries = 3

    for i in range(0, len(suburbs), batch_size):
        batch = suburbs[i:i+batch_size]
        lats = ','.join(str(round(s[2], 4)) for s in batch)
        lons = ','.join(str(round(s[3], 4)) for s in batch)
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lats}&longitude={lons}"
            f"&current=temperature_2m,apparent_temperature,uv_index"
            f"&timezone=Australia%2FSydney"
        )

        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(url, timeout=15) as resp:
                    data = json.loads(resp.read())
                    if isinstance(data, dict):
                        data = [data]
                    for j, item in enumerate(data):
                        results[batch[j][0]] = {
                            'temperature': item['current']['temperature_2m'],
                            'apparent_temperature': item['current']['apparent_temperature'],
                            'uv_index': item['current']['uv_index'],
                        }
                    break
            except Exception as e:
                print(f"Batch {i//batch_size + 1} attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    print(f"Skipping batch {i//batch_size + 1} after {max_retries} attempts")

    return results

def lambda_handler(event, context):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT suburb_id, suburb_name, latitude, longitude FROM Suburb")
    suburbs = cursor.fetchall()
    print(f"Fetching temperatures for {len(suburbs)} suburbs...")

    temp_map = fetch_temperatures_batch(suburbs)

    # 读取 vegetation 数据用于计算 shade_score
    cursor.execute("SELECT suburb_id, vegetation_index FROM Vegetation_Data")
    veg_map = {row[0]: float(row[1]) for row in cursor.fetchall()}

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE Heat_Data")
    cursor.execute("TRUNCATE TABLE Risk_Assessment")

    inserted = 0
    for suburb_id, suburb_name, lat, lon in suburbs:
        weather = temp_map.get(suburb_id)
        if weather is None:
            continue

        temp = weather['temperature']
        apparent_temp = weather['apparent_temperature']
        uv_index = weather['uv_index']

        heat_level = get_heat_level(apparent_temp)
        heat_score = get_heat_score(apparent_temp, uv_index)

        cursor.execute("""
            INSERT INTO Heat_Data (suburb_id, temperature, apparent_temperature, uv_index, heat_level)
            VALUES (%s, %s, %s, %s, %s)
        """, (suburb_id, temp, apparent_temp, uv_index, heat_level))

        shade_score = get_shade_score(veg_map.get(suburb_id, (VEG_MIN + VEG_MAX) / 2))
        combined = heat_score * 0.7 + shade_score * 0.3
        if combined >= 65:
            risk_level = 'high'
        elif combined >= 40:
            risk_level = 'moderate'
        else:
            risk_level = 'low'

        cursor.execute("""
            INSERT INTO Risk_Assessment (suburb_id, shade_score, heat_score, risk_level, generated_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (suburb_id, shade_score, heat_score, risk_level))

        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Done: {inserted} records updated")
    return {'statusCode': 200, 'body': json.dumps({'updated': inserted})}