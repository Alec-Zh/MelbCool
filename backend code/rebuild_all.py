import geopandas as gpd
import pymysql
import pandas as pd

# ── 配置 ──────────────────────────────────────────────
BASE = r"C:\Users\ALEC\Downloads"
HEAT_SHP   = BASE + r"\Order_MYM2F8\ll_gda2020\esrishape\whole_of_dataset\victoria\PLANNING\HEAT_URBAN_HEAT_2018.shp"
SA2_SHP = BASE + r"\SA2_2021_AUST_SHP_GDA2020\SA2_2021_AUST_GDA2020.shp"
ABS_BASE   = BASE + r"\2021_GCP_all_for_VIC_short-header\2021 Census GCP All Geographies for VIC\SA2\VIC"
GEO_DESC   = BASE + r"\2021_GCP_all_for_VIC_short-header\Metadata\2021Census_geog_desc_1st_2nd_3rd_release.xlsx"

DB_CONFIG = {
    "host": "heatmap.cbccg4mkeiln.ap-southeast-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": not shown,
    "database": "heatmap",
    "charset": "utf8mb4",
}

# ── 1. 读取并 spatial join ─────────────────────────────
print("Reading shapefiles...")
heat = gpd.read_file(HEAT_SHP).to_crs(epsg=7844)
sa2  = gpd.read_file(SA2_SHP).to_crs(epsg=7844)
mel  = sa2[sa2['GCC_CODE21'] == '2GMEL'].copy()

print("Spatial joining...")
heat_c = heat.copy()
heat_c['geometry'] = heat.to_crs(epsg=7844).geometry.centroid
joined = gpd.sjoin(heat_c, mel[['SA2_CODE21','SA2_NAME21','geometry']], how='inner', predicate='within')
print(f"  Matched {len(joined)} mesh blocks to {joined['SA2_NAME21'].nunique()} suburbs")

# ── 2. 聚合到 SA2 2021 级别 ───────────────────────────
print("Aggregating to SA2...")
suburb_agg = joined.groupby(['SA2_CODE21','SA2_NAME21']).agg(
    peranyveg_mean=('PERANYVEG', 'mean'),
).reset_index()

# 经纬度从SA2边界获取
mel_proj = mel.to_crs(epsg=4326)
mel_proj['centroid_lat'] = mel_proj.geometry.centroid.y
mel_proj['centroid_lon'] = mel_proj.geometry.centroid.x
coords = mel_proj[['SA2_CODE21','centroid_lat','centroid_lon']]
suburb_agg = suburb_agg.merge(coords, on='SA2_CODE21')
print(f"  {len(suburb_agg)} suburbs ready")

# ── 3. 读取人口数据 ────────────────────────────────────
print("Reading census data...")
geo = pd.read_excel(GEO_DESC, sheet_name='2021_ASGS_MAIN_Structures')
sa2_map = geo[geo['ASGS_Structure']=='SA2'][['Census_Code_2021','Census_Name_2021']].copy()
sa2_map['Census_Code_2021'] = sa2_map['Census_Code_2021'].astype(str)

g01 = pd.read_csv(ABS_BASE + r"\2021Census_G01_VIC_SA2.csv")[['SA2_CODE_2021','Tot_P_P']]
g01['SA2_CODE_2021'] = g01['SA2_CODE_2021'].astype(str)

g04b = pd.read_csv(ABS_BASE + r"\2021Census_G04B_VIC_SA2.csv")
age60_cols = [c for c in g04b.columns if c.endswith('_P') and
              any(str(x) in c for x in ['60','65','70','75','80','85'])]
g04b['elderly_population'] = g04b[age60_cols].sum(axis=1)
g04b = g04b[['SA2_CODE_2021','elderly_population']]
g04b['SA2_CODE_2021'] = g04b['SA2_CODE_2021'].astype(str)

pop = g01.merge(g04b, on='SA2_CODE_2021')
pop = pop.merge(sa2_map, left_on='SA2_CODE_2021', right_on='Census_Code_2021')
pop = pop.rename(columns={'Tot_P_P':'total_population'})
# 用SA2_CODE匹配（更准确）
pop_dict = dict(zip(pop['SA2_CODE_2021'], zip(pop['total_population'], pop['elderly_population'])))

# ── 4. 清空旧数据并重新导入 ──────────────────────────
print("\nConnecting to DB...")
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

print("Clearing old data...")
cursor.execute("SET FOREIGN_KEY_CHECKS=0")
cursor.execute("TRUNCATE TABLE Population_Data")
cursor.execute("TRUNCATE TABLE Vegetation_Data")
cursor.execute("TRUNCATE TABLE Suburb")
cursor.execute("SET FOREIGN_KEY_CHECKS=1")

# Suburb
print("Inserting Suburb...")
suburb_id_map = {}
for _, row in suburb_agg.iterrows():
    cursor.execute(
        "INSERT INTO Suburb (suburb_name, latitude, longitude) VALUES (%s, %s, %s)",
        (row['SA2_NAME21'], round(row['centroid_lat'], 6), round(row['centroid_lon'], 6))
    )
    suburb_id_map[row['SA2_CODE21']] = cursor.lastrowid
print(f"  Inserted {len(suburb_id_map)} suburbs")

# Vegetation_Data
print("Inserting Vegetation_Data...")
for _, row in suburb_agg.iterrows():
    sid = suburb_id_map[row['SA2_CODE21']]
    cursor.execute(
        "INSERT INTO Vegetation_Data (suburb_id, vegetation_index, year) VALUES (%s, %s, %s)",
        (sid, round(row['peranyveg_mean'], 4), 2018)
    )
print(f"  Inserted {len(suburb_agg)} vegetation records")

# Population_Data
print("Inserting Population_Data...")
count, skipped = 0, 0
for sa2_code, sid in suburb_id_map.items():
    if sa2_code in pop_dict:
        total_pop, elderly_pop = pop_dict[sa2_code]
        cursor.execute(
            "INSERT INTO Population_Data (suburb_id, total_population, elderly_population, year) VALUES (%s, %s, %s, %s)",
            (sid, int(total_pop), int(elderly_pop), 2021)
        )
        count += 1
    else:
        skipped += 1
print(f"  Inserted {count}, skipped {skipped}")

conn.commit()
cursor.close()
conn.close()
print("\nAll done!")