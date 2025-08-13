import json

# Load enriched file with multiple scores
with open("location_scored_listings.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Calculate composite score and price ratio
ranked = []
for home in listings:
    drive = home.get("driveabilityScore", 0)
    loc = home.get("customLocationScore", 0)

    # Add more scores as needed, e.g.:
    # tech = home.get("techProximityScore", 0)
    # roi_type = home.get("roiPropertyTypeScore", 0)

    # Define custom composite score (equal weight for now)
    composite = round(0.5 * drive + 0.5 * loc, 4)

    price = home.get("price")
    if price and price > 0:
        value_ratio = round(composite / price, 8)
        home["compositeScore"] = composite
        home["pricePerCompositeScore"] = value_ratio
        ranked.append(home)

# Sort by best value per dollar
ranked.sort(key=lambda x: x["pricePerCompositeScore"], reverse=True)

# Save
with open("ranked_by_composite_value.json", "w", encoding="utf-8") as f:
    json.dump(ranked, f, indent=2)

# Print top 10
print("Top Composite ROI Value Homes:")
for i, home in enumerate(ranked[:10], 1):
    print(f"{i}. {home.get('streetAddress')} | ${home.get('price')} | "
          f"Composite: {home['compositeScore']} | "
          f"Ratio: {home['pricePerCompositeScore']}")
