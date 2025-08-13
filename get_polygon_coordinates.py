from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point
import time

# List of ZIPs
zip_codes = ["78701", "78703", "78704", "78702", "78745", "78756"]

# Setup geolocator
geolocator = Nominatim(user_agent="zip-buffer")

# Store results
polygons = []

for zip_code in zip_codes:
    location = geolocator.geocode(f"{zip_code}, Austin, TX")
    if location:
        point = Point(location.longitude, location.latitude)
        buffer = point.buffer(0.01)  # ~1km radius
        coords = list(buffer.exterior.coords)
        polygon_str = ",".join([f"{lat} {lng}" for lng, lat in coords])
        polygons.append(f"{zip_code}: {polygon_str}")
        print(f"✓ Got polygon for {zip_code}")
    else:
        print(f"✗ Could not find {zip_code}")
    time.sleep(1)  # Nominatim rate limit

# Save to TXT
with open("zip_polygons_buffered.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(polygons))

print("Saved to zip_polygons_buffered.txt")
