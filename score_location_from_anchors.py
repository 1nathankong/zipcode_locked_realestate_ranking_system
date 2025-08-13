import json
from math import radians, cos, sin, sqrt, atan2

# ---- CONFIG ----
INPUT_FILE = "top_driveable_listings2.json"
OUTPUT_FILE = "location_scored_listings.json"
MAX_DISTANCE_KM = 15
# ----------------

# 🎯 Anchor points (lat, lon) — edit/add as needed
anchors = {
    "downtown": (30.2672, -97.7431),
    "domain": (30.4016, -97.7240),
    "oracle": (30.2442, -97.7162),
    "tesla": (30.2210, -97.5860),
    "barton": (30.2603, -97.7720),
    "nvidia": (30.3840, -97.7290),
    "amd": (30.2666, -97.8650),
    "ut_austin": (30.2849, -97.7341),
    "capital_factory": (30.2673, -97.7416)
}

# 🧮 Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

# 📈 Score based on distance to all anchors
def score_location(lat, lon):
    scores = []
    for _, (a_lat, a_lon) in anchors.items():
        dist = haversine(lat, lon, a_lat, a_lon)
        score = max(0, 1 - dist / MAX_DISTANCE_KM)
        scores.append(score)
    return round(sum(scores) / len(scores), 4)

# 🧾 Load listings
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    listings = json.load(f)

# 🧠 Compute and add scores
for listing in listings:
    lat = listing.get("latitude")
    lon = listing.get("longitude")
    if lat is not None and lon is not None:
        listing["customLocationScore"] = score_location(lat, lon)
    else:
        listing["customLocationScore"] = None

# 💾 Save to output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(listings, f, indent=2)

print(f"✅ Scored {len(listings)} properties by location and saved to {OUTPUT_FILE}")
