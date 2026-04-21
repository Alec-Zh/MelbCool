import geopandas as gpd
import pymysql
import pandas as pd

# ── Config ────────────────────────────────────────────
BASE = r"C:\Users\ALEC\Downloads"

HEAT_SHP = BASE + r"\Order_MYM2F8\ll_gda2020\esrishape\whole_of_dataset\victoria\PLANNING\HEAT_URBAN_HEAT_2018.shp"
SAL_SHP  = BASE + r"\SAL_2021_AUST_GDA2020_SHP\SAL_2021_AUST_GDA2020.shp"
ABS_BASE = BASE + r"\2021_GCP_all_for_VIC_short-header\2021 Census GCP All Geographies for VIC\SAL\VIC"

DB_CONFIG = {
    "host": "heatmap.cbccg4mkeiln.ap-southeast-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
     "password": not shown,
    "database": "heatmap",
    "charset": "utf8mb4",
}

# ── 1. Load SAL boundary (Victoria only) ─────────────
print("Reading SAL shapefile...")
sal = gpd.read_file(SAL_SHP).to_crs(epsg=7844)
vic_sal = sal[sal['STE_CODE21'] == '2'].copy()
print(f"  {len(vic_sal)} VIC SAL suburbs loaded")

# ── 2. Spatial join: heat mesh blocks → SAL ──────────
print("Reading heat shapefile...")
heat = gpd.read_file(HEAT_SHP).to_crs(epsg=7844)

print("Spatial joining mesh blocks to SAL...")
heat_c = heat.copy()
heat_c['geometry'] = heat_c.geometry.centroid
joined = gpd.sjoin(
    heat_c,
    vic_sal[['SAL_CODE21', 'SAL_NAME21', 'geometry']],
    how='inner',
    predicate='within'
)
print(f"  Matched {len(joined)} mesh blocks to {joined['SAL_NAME21'].nunique()} SAL suburbs")

# ── 3. Aggregate vegetation to SAL ───────────────────
print("Aggregating vegetation data to SAL...")
sal_agg = joined.groupby(['SAL_CODE21', 'SAL_NAME21']).agg(
    peranyveg_mean=('PERANYVEG', 'mean'),
).reset_index()

# Add centroid lat/lon from SAL boundary
vic_sal_4326 = vic_sal.to_crs(epsg=4326).copy()
vic_sal_4326['centroid_lat'] = vic_sal_4326.geometry.centroid.y
vic_sal_4326['centroid_lon'] = vic_sal_4326.geometry.centroid.x
coords = vic_sal_4326[['SAL_CODE21', 'centroid_lat', 'centroid_lon']]
sal_agg = sal_agg.merge(coords, on='SAL_CODE21')
print(f"  {len(sal_agg)} suburbs with vegetation data")

# ── 4. Load population data (SAL) ────────────────────
print("Reading Census G01 (total population)...")
g01 = pd.read_csv(ABS_BASE + r"\2021Census_G01_VIC_SAL.csv")[['SAL_CODE_2021', 'Tot_P_P']]
# Strip 'SAL' prefix to match shapefile code format
g01['SAL_CODE21'] = g01['SAL_CODE_2021'].str.replace('SAL', '', regex=False)

print("Reading Census G04B (age by sex)...")
g04b = pd.read_csv(ABS_BASE + r"\2021Census_G04B_VIC_SAL.csv")
g04b['SAL_CODE21'] = g04b['SAL_CODE_2021'].str.replace('SAL', '', regex=False)

# Sum single-year age columns 60-99 to avoid double-counting with grouped columns
age60_cols = [c for c in g04b.columns
              if c.endswith('_P') and
              any(f'Age_yr_{x}_P' == c for x in range(60, 100))]
# Fallback: use grouped columns if single-year not available
if not age60_cols:
    age60_cols = [c for c in g04b.columns if c.endswith('_P') and
                  any(str(x) in c for x in ['60','65','70','75','80','85'])]
    print(f"  Using grouped age columns: {age60_cols}")
else:
    print(f"  Using {len(age60_cols)} single-year age columns (60-99)")

g04b['elderly_population'] = g04b[age60_cols].sum(axis=1)
g04b = g04b[['SAL_CODE21', 'elderly_population']]

pop = g01.merge(g04b, on='SAL_CODE21')
pop = pop.rename(columns={'Tot_P_P': 'total_population'})
pop_dict = dict(zip(pop['SAL_CODE21'], zip(pop['total_population'], pop['elderly_population'])))
print(f"  {len(pop_dict)} suburbs with population data")

# ── 5. Clear and repopulate DB ───────────────────────
print("\nConnecting to DB...")
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

print("Clearing old data...")
cursor.execute("SET FOREIGN_KEY_CHECKS=0")
for table in ['Risk_Assessment', 'Heat_Data', 'Population_Data', 'Vegetation_Data', 'Suburb']:
    cursor.execute(f"TRUNCATE TABLE {table}")
cursor.execute("SET FOREIGN_KEY_CHECKS=1")

# Insert Suburb
print("Inserting Suburb...")
suburb_id_map = {}
for _, row in sal_agg.iterrows():
    cursor.execute(
        "INSERT INTO Suburb (suburb_name, latitude, longitude) VALUES (%s, %s, %s)",
        (row['SAL_NAME21'], round(row['centroid_lat'], 6), round(row['centroid_lon'], 6))
    )
    suburb_id_map[row['SAL_CODE21']] = cursor.lastrowid
print(f"  Inserted {len(suburb_id_map)} suburbs")

# Insert Vegetation_Data
print("Inserting Vegetation_Data...")
for _, row in sal_agg.iterrows():
    sid = suburb_id_map[row['SAL_CODE21']]
    cursor.execute(
        "INSERT INTO Vegetation_Data (suburb_id, vegetation_index, year) VALUES (%s, %s, %s)",
        (sid, round(row['peranyveg_mean'], 4), 2018)
    )
print(f"  Inserted {len(sal_agg)} vegetation records")

# Insert Population_Data
print("Inserting Population_Data...")
count, skipped = 0, 0
for sal_code, sid in suburb_id_map.items():
    if sal_code in pop_dict:
        total_pop, elderly_pop = pop_dict[sal_code]
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