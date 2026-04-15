"""
Export inner Melbourne SAL boundaries as GeoJSON for the frontend map.
Filters by LGA to get inner Melbourne suburbs only — no DB connection needed.

Output: melbourne-suburbs.geojson  (drop into /public/geojson/)
"""
import geopandas as gpd
import json

BASE    = r"C:\Users\ALEC\Downloads"
SAL_SHP = BASE + r"\SAL_2021_AUST_GDA2020_SHP\SAL_2021_AUST_GDA2020.shp"
LGA_SHP = BASE + r"\LGA_2021_AUST_GDA2020_SHP\LGA_2021_AUST_GDA2020.shp"
OUTPUT  = BASE + r"\melbourne-suburbs.geojson"

# Inner Melbourne LGAs — adjust this list if you want a wider/narrower scope
INNER_MELBOURNE_LGAS = {
    'Melbourne',
    'Yarra',
    'Port Phillip',
    'Stonnington',
    'Moonee Valley',
    'Moreland',   # renamed to Merri-bek in 2022; use whichever name appears in your LGA file
}

# ── 1. Load LGA and filter to inner Melbourne ────────
print("Loading LGA shapefile...")
lga = gpd.read_file(LGA_SHP).to_crs(epsg=7844)

# LGA_NAME21 format is e.g. "Melbourne (C)", "Yarra (C)" — strip the suffix
lga['lga_short'] = lga['LGA_NAME21'].str.replace(r'\s*\(.*\)', '', regex=True).str.strip()
inner_lga = lga[lga['lga_short'].isin(INNER_MELBOURNE_LGAS)].copy()
print(f"  Matched LGAs: {sorted(inner_lga['LGA_NAME21'].tolist())}")

# Dissolve into a single boundary polygon
inner_boundary = inner_lga.dissolve()

# ── 2. Load SAL (VIC only) and filter by centroid ───
print("Loading SAL shapefile (VIC)...")
sal = gpd.read_file(SAL_SHP).to_crs(epsg=7844)
vic_sal = sal[sal['STE_CODE21'] == '2'].copy()

# Keep SAL suburbs whose centroid falls within the inner Melbourne boundary
vic_sal = vic_sal.copy()
vic_sal['centroid'] = vic_sal.geometry.centroid
inner_sal = vic_sal[vic_sal['centroid'].within(inner_boundary.geometry.iloc[0])].copy()

print(f"\n  {len(inner_sal)} inner Melbourne SAL suburbs:")
for name in sorted(inner_sal['SAL_NAME21'].tolist()):
    print(f"    {name}")

# ── 3. Export as GeoJSON ─────────────────────────────
print("\nExporting GeoJSON...")
inner_sal_4326 = inner_sal.to_crs(epsg=4326)

features = []
for _, row in inner_sal_4326.iterrows():
    features.append({
        "type": "Feature",
        "properties": {
            "name": row['SAL_NAME21'],
            "sal_code": row['SAL_CODE21'],
        },
        "geometry": row['geometry'].__geo_interface__
    })

geojson = {"type": "FeatureCollection", "features": features}

with open(OUTPUT, 'w') as f:
    json.dump(geojson, f)

print(f"\nExported {len(features)} suburbs to: {OUTPUT}")
print("Copy to /public/geojson/melbourne-suburbs.geojson in the frontend project.")