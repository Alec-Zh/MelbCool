import pymysql

DB_CONFIG = {
    "host": "heatmap.cbccg4mkeiln.ap-southeast-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": "insert your password here",
    "database": "heatmap",
    "charset": "utf8mb4",
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# 读取所有 suburb 的植被数据
cursor.execute("""
    SELECT s.suburb_id, v.vegetation_index
    FROM Suburb s
    JOIN Vegetation_Data v ON s.suburb_id = v.suburb_id
""")
rows = cursor.fetchall()
print(f"Found {len(rows)} suburbs with vegetation data")

count = 0
for suburb_id, veg_index in rows:
    # shade_score 只基于树冠覆盖率 (vegetation_index = PERANYVEG, 0-100)
    shade_score = round(float(veg_index), 2)

    # heat_score 暂时为 0，等 Lambda 实时更新
    cursor.execute("""
        INSERT INTO Risk_Assessment (suburb_id, heat_score, shade_score, risk_level)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE shade_score = VALUES(shade_score)
    """, (suburb_id, 0.00, shade_score, 'moderate'))
    count += 1

conn.commit()
cursor.close()
conn.close()
print(f"Inserted/updated {count} shade_score records")
print("Done!")