import json
import requests
import time
from math import radians, cos, sin, sqrt, atan2

# Haversine distance helper
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

# OSM Overpass query
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
    response = requests.post(url, data=query)
    time.sleep(1)
    return response.json().get("elements", [])

# Extract and format results with distance
def get_nearby_places(listing, tags, label, radius=7000):
    lat, lon = listing["latitude"], listing["longitude"]
    elements = query_osm(lat, lon, radius, tags)
    places = []
    for el in elements:
        name = el.get("tags", {}).get("name", "Unnamed")
        distance = round(haversine(lat, lon, el["lat"], el["lon"]), 3)
        places.append({"name": name, "distance_km": distance})
    return sorted(places, key=lambda x: x["distance_km"])

# Tags to search
grocery_tags = [("shop", "supermarket"), ("amenity", "grocery_store")]
gym_tags = [("leisure", "fitness_centre"), ("leisure", "sports_centre"), ("amenity", "gym")]

# Load your listings
with open("filtered_for_sale_by_zip.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Enrich each listing
for listing in listings:
    try:
        lat, lon = listing["latitude"], listing["longitude"]
        if lat and lon:
            listing["groceryStores"] = get_nearby_places(listing, grocery_tags, "grocery")
            listing["gyms"] = get_nearby_places(listing, gym_tags, "gym")
            print(f"Processed {listing.get('streetAddress', 'unknown')}")
    except Exception as e:
        print(f"Error processing property: {e}")
        listing["groceryStores"] = []
        listing["gyms"] = []

# Save enriched data
with open("enriched_with_distances2.json", "w", encoding="utf-8") as f:
    json.dump(listings, f, indent=2)

print("Saved enriched_with_distances2.json")
