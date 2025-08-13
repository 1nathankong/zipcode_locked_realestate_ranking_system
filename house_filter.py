import json
import os

# Define your 6 target ZIP codes
target_zipcodes = {"78701", "78703", "78704", "78702", "78745", "78756"}

# Optional: allowed home types
allowed_types = {"SINGLE_FAMILY", "MULTI_FAMILY", "DUPLEX"}

# Directory with saved Zillow JSONs
input_dir = "./"
filtered_listings = []

# Loop through all zillow_*.json files
for file_name in os.listdir(input_dir):
    if file_name.startswith("zillow_") and file_name.endswith(".json"):
        with open(os.path.join(input_dir, file_name), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for home in data.get("results", []):
                    zip_code = home.get("zipcode")
                    status = home.get("homeStatus", "").upper()
                    subtypes = home.get("listing_sub_type", {})
                    home_type = home.get("homeType", "")

                    if (
                        zip_code in target_zipcodes and
                        status == "FOR_SALE" and
                        subtypes.get("is_FSBA", False) and
                        home_type in allowed_types
                    ):
                        filtered_listings.append(home)

            except json.JSONDecodeError:
                print(f"⚠️ Skipping invalid file: {file_name}")

# Save filtered output
with open("filtered_for_sale_by_zip.json", "w", encoding="utf-8") as f:
    json.dump(filtered_listings, f, indent=2)

print(f"Saved {len(filtered_listings)} listings to filtered_for_sale_by_zip.json")
