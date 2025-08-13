import http.client
import json
import urllib.parse
import time

# Your Zillow56 API credentials
headers = {
    'x-rapidapi-key': "c22beff351msh99ffd131e29f780p1ba84bjsn84e84efefd1a",
    'x-rapidapi-host': "zillow56.p.rapidapi.com"
}

# Load polygon definitions from your buffered polygon text file
with open("zip_polygons_buffered.txt", "r", encoding="utf-8") as f:
    polygon_lines = f.read().strip().split("\n\n")

# Initialize connection
conn = http.client.HTTPSConnection("zillow56.p.rapidapi.com")

# Iterate over each ZIP polygon
for line in polygon_lines:
    try:
        zip_code, raw_coords = line.split(": ")
        encoded_polygon = urllib.parse.quote(raw_coords)

        print(f"Requesting listings for ZIP {zip_code}...")

        # Build and send request
        url = f"/search_polygon?polygon={encoded_polygon}&output=json&status=forSale&sortSelection=priorityscore&listing_type=by_agent&doz=any"
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read()

        # Try parsing response as JSON
        try:
            parsed = json.loads(data)
            # Save each ZIP's result in its own file
            with open(f"zillow_{zip_code}.json", "w", encoding="utf-8") as f_out:
                json.dump(parsed, f_out, indent=2)
            print(f"Saved results to zillow_{zip_code}.json")
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for ZIP {zip_code}")

        # Respect API rate limits
        time.sleep(1)

    except Exception as e:
        print(f"Error processing ZIP line: {line}")
        print(str(e))
        continue

conn.close()
