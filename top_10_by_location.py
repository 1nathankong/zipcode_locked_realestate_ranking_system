import json

# Load scored listings
with open("location_scored_listings.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Sort by location score (descending)
sorted_listings = sorted(
    [l for l in listings if l.get("customLocationScore") is not None],
    key=lambda x: x["customLocationScore"],
    reverse=True
)

# Print top 10
print("🏆 Top 10 Properties by Location Score:\n")
for i, l in enumerate(sorted_listings[:10], 1):
    address = l.get("streetAddress", "Unknown")
    score = l["customLocationScore"]
    price = l.get("price", "N/A")
    print(f"{i}. {address} | ${price} | Location Score: {score}")
