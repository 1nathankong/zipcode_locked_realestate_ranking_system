import json

# Load scored listings
with open("location_scored_listings.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Optional: recompute compositeScore (if needed)
for home in listings:
    drive = home.get("driveabilityScore", 0)
    loc = home.get("customLocationScore", 0)
    home["compositeScore"] = round(0.5 * drive + 0.5 * loc, 4)

# 🟢 Filter by price under $700,000
filtered = [h for h in listings if h.get("price") and h["price"] <= 700000]

# Sort by compositeScore (highest first)
ranked = sorted(
    [h for h in filtered if h.get("compositeScore") is not None],
    key=lambda x: x["compositeScore"],
    reverse=True
)

# Save top results
with open("ranked_by_composite_score_under700k.json", "w", encoding="utf-8") as f:
    json.dump(ranked, f, indent=2)

# Print top 10
print("🏆 Top Properties by Composite Score (Under $700K):")
for i, home in enumerate(ranked[:10], 1):
    addr = home.get("streetAddress", "Unknown")
    price = home.get("price", "N/A")
    score = home.get("compositeScore")
    print(f"{i}. {addr} | ${price} | Composite Score: {score}")
