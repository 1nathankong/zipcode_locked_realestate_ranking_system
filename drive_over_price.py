import json

# Load driveability-enriched properties
with open("enriched_final_driveability2.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Calculate ratio and filter out invalid entries
ranked = []
for home in listings:
    score = home.get("driveabilityScore")
    price = home.get("price")

    if score and price and price > 0:
        rating = round(score / price, 8)  # smaller value = higher price sensitivity
        home["pricePerDriveability"] = rating
        ranked.append(home)

# Sort descending — best value (highest driveability per dollar) at top
ranked.sort(key=lambda x: x["pricePerDriveability"], reverse=True)

# Save result
with open("ranked_by_driveability_value.json", "w", encoding="utf-8") as f:
    json.dump(ranked, f, indent=2)

# Print top 10
print("Top Best Driveability Value Homes:")
for i, home in enumerate(ranked[:101], 1):
    addr = home.get("streetAddress", "Unknown")
    score = home.get("driveabilityScore")
    price = home.get("price")
    ratio = home.get("pricePerDriveability")
    print(f"{i}. {addr} | ${price} | Driveability: {score} | Ratio: {ratio}")
