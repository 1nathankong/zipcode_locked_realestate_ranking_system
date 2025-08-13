import json

# Load enriched listings
with open("enriched_with_distances2.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Filter condition: max price $1.4M, and optionally: must have at least one gym/grocery
filtered = []
for home in listings:
    price = home.get("price", 0)
    groceries = home.get("groceryStores", [])
    gyms = home.get("gyms", [])
    
    if (
        price <= 1600000 and
        groceries and
        gyms
    ):
        filtered.append(home)

# Save the filtered list
with open("final_filtered_properties.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)

print(f"✅ Saved {len(filtered)} homes under $1.4M with nearby gyms and grocery stores.")
