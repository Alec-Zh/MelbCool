import pymysql

DB_CONFIG = {
    "host": "heatmap.cbccg4mkeiln.ap-southeast-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
     "password": not shown,
    "database": "heatmap",
    "charset": "utf8mb4",
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# 读取所有 suburb 的人口和植被数据
cursor.execute("""
    SELECT 
        s.suburb_id,
        p.elderly_population,
        p.total_population,
        v.vegetation_index
    FROM Suburb s
    JOIN Population_Data p ON s.suburb_id = p.suburb_id
    JOIN Vegetation_Data v ON s.suburb_id = v.suburb_id
""")
rows = cursor.fetchall()
print(f"Found {len(rows)} suburbs with full data")

count = 0
for suburb_id, elderly_pop, total_pop, veg_index in rows:
    # 老龄化比例分 (0-50)
    elderly_ratio = (elderly_pop / total_pop) if total_pop > 0 else 0
    age_score = min(elderly_ratio * 200, 50)  # 25%老龄化 = 满分50

    # 植被缺乏分 (0-50)
    veg_score = min((100 - float(veg_index)) * 0.5, 50)

    # 综合 vulnerability_score (0-100)
    vulnerability_score = round(age_score + veg_score, 2)

    # risk_level 分级
    if vulnerability_score >= 65:
        risk_level = 'high'
    elif vulnerability_score >= 40:
        risk_level = 'moderate'
    else:
        risk_level = 'low'

    # heat_score 暂时为 0，等 Lambda 实时更新
    cursor.execute("""
        INSERT INTO Risk_Assessment (suburb_id, heat_score, vulnerability_score, risk_level)
        VALUES (%s, %s, %s, %s)
    """, (suburb_id, 0.00, vulnerability_score, risk_level))
    count += 1

conn.commit()
cursor.close()
conn.close()
print(f"Inserted {count} risk assessment records")
print("Done!")