import pymysql
import pandas as pd

# ── 配置 ──────────────────────────────────────────────
BASE = r"C:\Users\ALEC\Downloads"
ABS_BASE = BASE + r"\2021_GCP_all_for_VIC_short-header\2021 Census GCP All Geographies for VIC\SA2\VIC"
GEO_DESC = BASE + r"\2021_GCP_all_for_VIC_short-header\Metadata\2021Census_geog_desc_1st_2nd_3rd_release.xlsx"

DB_CONFIG = {
    "host": "heatmap.cbccg4mkeiln.ap-southeast-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": not shown,
    "database": "heatmap",
    "charset": "utf8mb4",
}

# ── 1. 从数据库读取已有的 suburb_id ────────────────────
print("Fetching existing suburbs from DB...")
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("SELECT suburb_id, suburb_name FROM Suburb")
suburb_id_map = {name: sid for sid, name in cursor.fetchall()}
print(f"  Found {len(suburb_id_map)} suburbs in DB")

# ── 2. 读取人口数据 ────────────────────────────────────
print("Reading census data...")
geo = pd.read_excel(GEO_DESC, sheet_name='2021_ASGS_MAIN_Structures')
sa2_map = geo[geo['ASGS_Structure']=='SA2'][['Census_Code_2021','Census_Name_2021']].copy()
sa2_map['Census_Code_2021'] = sa2_map['Census_Code_2021'].astype(int)

g01 = pd.read_csv(ABS_BASE + r"\2021Census_G01_VIC_SA2.csv")[['SA2_CODE_2021','Tot_P_P']]
g01 = g01.merge(sa2_map, left_on='SA2_CODE_2021', right_on='Census_Code_2021')

g04b = pd.read_csv(ABS_BASE + r"\2021Census_G04B_VIC_SA2.csv")
age60_cols = [c for c in g04b.columns if c.endswith('_P') and
              any(str(x) in c for x in ['60','65','70','75','80','85'])]
g04b['elderly_population'] = g04b[age60_cols].sum(axis=1)
g04b = g04b[['SA2_CODE_2021','elderly_population']]

pop = g01.merge(g04b, on='SA2_CODE_2021')
pop = pop.rename(columns={'Tot_P_P':'total_population','Census_Name_2021':'suburb_name'})
pop_dict = dict(zip(pop['suburb_name'], zip(pop['total_population'], pop['elderly_population'])))
print(f"  {len(pop_dict)} suburbs in census data")

# ── 3. 插入 Population_Data ────────────────────────────
print("Inserting Population_Data...")
count, skipped = 0, 0
for suburb_name, sid in suburb_id_map.items():
    if suburb_name in pop_dict:
        total_pop, elderly_pop = pop_dict[suburb_name]
        cursor.execute(
            "INSERT INTO Population_Data (suburb_id, total_population, elderly_population, year) VALUES (%s, %s, %s, %s)",
            (sid, int(total_pop), int(elderly_pop), 2021)
        )
        count += 1
    else:
        skipped += 1

conn.commit()
cursor.close()
conn.close()
print(f"  Inserted {count} records, skipped {skipped} (no census match)")
print("\nDone!")