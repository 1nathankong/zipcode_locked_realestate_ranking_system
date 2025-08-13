import json
import requests
import time
from math import radians, cos, sin, sqrt, atan2

# -------------------- CONFIG --------------------
INPUT_FILE = "final_filtered_properties.json"
OUTPUT_FILE = "enriched_final_driveability2.json"
SLEEP_BETWEEN_CALLS = 1  # seconds
# ------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def query_osm(lat, lon, radius_m, tags):
    tag_blocks = "\n".join([
        f'node["{tag[0]}"="{tag[1]}"](around:{radius_m},{lat},{lon});'
        for tag in tags
    ])
    query = f"""
    [out:json];
    (
      {tag_blocks}
    );
    out center;
    """
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(url, data=query, timeout=30)
        time.sleep(1.5)  # Optional: increase to avoid rate limiting

        if not response.text.strip():
            print(f"⚠️ Blank response for lat={lat}, lon={lon}")
            return []

        return response.json().get("elements", [])

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request error for lat={lat}, lon={lon}: {e}")
        return []
    except json.JSONDecodeError:
        print(f"⚠️ JSON decode error for lat={lat}, lon={lon}")
        return []


def score_driveability(highway_km, garage_spaces, gas_count, drive_thru_count):
    if highway_km < 0.2:
        h_score = 0.2  # too close = noise penalty
    elif 0.2 <= highway_km <= 1.0:
        h_score = 1.0  # ideal range
    elif highway_km <= 5.0:
        h_score = 1 - ((highway_km - 1) / 4)  # fades from 1.0 to 0.0
    else:
        h_score = 0.0  # too far

    g_score = min((garage_spaces or 0) / 2, 1.0)  # 2+ garage = full
    f_score = min(gas_count / 3, 1.0)  # 3+ gas = full
    d_score = min(drive_thru_count / 2, 1.0)  # 2+ = full
    return round(0.4 * h_score + 0.3 * g_score + 0.2 * f_score + 0.1 * d_score, 3)

# Tags
highway_tags = [("highway", "motorway"), ("highway", "trunk"), ("highway", "primary")]
gas_tags = [("amenity", "fuel")]
drive_thru_tags = [("amenity", "fast_food"), ("drive_through", "yes")]

# Load properties
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    homes = json.load(f)

for home in homes:
    lat, lon = home.get("latitude"), home.get("longitude")
    if not lat or not lon:
        continue

    # Query OSM data
    highways = query_osm(lat, lon, 5000, highway_tags)
    highway_dists = [haversine(lat, lon, h["lat"], h["lon"]) for h in highways if "lat" in h and "lon" in h]
    min_highway = min(highway_dists) if highway_dists else 10

    gas_stations = query_osm(lat, lon, 2000, gas_tags)
    drive_thrus = query_osm(lat, lon, 2000, drive_thru_tags)

    # Compute score
    garage = home.get("garageSpaces", 0)
    drive_score = score_driveability(min_highway, garage, len(gas_stations), len(drive_thrus))

    # Store results
    home["driveabilityScore"] = drive_score
    home["nearestHighwayKm"] = round(min_highway, 3)
    home["gasStationsNearby"] = len(gas_stations)
    home["driveThrusNearby"] = len(drive_thrus)

# Save output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(homes, f, indent=2)

print(f"Saved driveability-enriched data to: {OUTPUT_FILE}")
