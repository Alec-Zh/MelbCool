import geopandas as gpd
import pymysql
import pandas as pd

# ── 配置 ──────────────────────────────────────────────
SHP_PATH = r"C:\Users\ALEC\Downloads\Order_MYM2F8\ll_gda2020\esrishape\whole_of_dataset\victoria\PLANNING\HEAT_URBAN_HEAT_2018.shp"
DB_CONFIG = {
    "host": "heatmap.cbccg4mkeiln.ap-southeast-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": not shown,
    "database": "heatmap",
    "charset": "utf8mb4",
}

# ── 读取 SHP ──────────────────────────────────────────
print("Reading shapefile...")
gdf = gpd.read_file(SHP_PATH)
gdf = gdf.to_crs(epsg=4326)

# ── 聚合到 suburb 级别 ────────────────────────────────
print("Aggregating to suburb level...")
suburb_agg = gdf.groupby("SA2_NAME16").agg(
    centroid_lat=("geometry", lambda g: g.centroid.y.mean()),
    centroid_lon=("geometry", lambda g: g.centroid.x.mean()),
    peranyveg_mean=("PERANYVEG", "mean"),
).reset_index()

print(f"Total suburbs: {len(suburb_agg)}")

# ── 导入数据库 ────────────────────────────────────────
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# 1. 导入 Suburb 表
print("\nInserting into Suburb table...")
suburb_id_map = {}

for _, row in suburb_agg.iterrows():
    cursor.execute(
        "INSERT INTO Suburb (suburb_name, latitude, longitude) VALUES (%s, %s, %s)",
        (row["SA2_NAME16"], round(row["centroid_lat"], 6), round(row["centroid_lon"], 6))
    )
    suburb_id_map[row["SA2_NAME16"]] = cursor.lastrowid

print(f"  Inserted {len(suburb_id_map)} suburbs")

# 2. 导入 Vegetation_Data 表
print("Inserting into Vegetation_Data table...")
for _, row in suburb_agg.iterrows():
    sid = suburb_id_map[row["SA2_NAME16"]]
    cursor.execute(
        "INSERT INTO Vegetation_Data (suburb_id, vegetation_index, year) VALUES (%s, %s, %s)",
        (sid, round(row["peranyveg_mean"], 4), 2018)
    )

print(f"  Inserted {len(suburb_agg)} vegetation records")

conn.commit()
cursor.close()
conn.close()
print("\nDone!")