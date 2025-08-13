import json

# Load enriched file
with open("enriched_final_driveability2.json", "r", encoding="utf-8") as f:
    listings = json.load(f)

# Sort by driveabilityScore (descending)
ranked = sorted(listings, key=lambda x: x.get("driveabilityScore", 0), reverse=True)

# Optional: save top N to a separate file
top_n = 101  # or any number you want
with open("top_driveable_listings2.json", "w", encoding="utf-8") as f:
    json.dump(ranked[:top_n], f, indent=2)

# Print summary of top results
for i, listing in enumerate(ranked[:101], 1):  # show top 10 in terminal
    print(f"{i}. {listing.get('streetAddress', 'Unknown')} | ZIP: {listing.get('zipcode')} | "
          f"Score: {listing['driveabilityScore']} | Price: ${listing.get('price')}")
