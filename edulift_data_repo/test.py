import pandas as pd
import time
import os
from geopy.geocoders import Nominatim

# Example test data (just 3 points in Rome, Italy)
data = {
    "lat": [54.075388],
    "lon": [9.979615]
}
df = pd.DataFrame(data)

OUTPUT_FILE = "data/processed/gps_traces_matched_test.csv"

def reverse_geocode_single(df, output_file=OUTPUT_FILE):
    print(f"📂 Loaded {len(df)} GPS test points")

    geolocator = Nominatim(user_agent="edulift_test")

    results = []
    for idx, (lat, lon) in enumerate(zip(df["lat"], df["lon"])):
        try:
            location = geolocator.reverse((lat, lon), exactly_one=True, language="en")
            if location and "road" in location.raw.get("address", {}):
                road_name = location.raw["address"]["road"]
            else:
                road_name = "unknown"
            results.append([lat, lon, location.latitude, location.longitude, road_name])
            print(f"✅ Point {idx+1}/{len(df)} → {road_name}")
        except Exception as e:
            print(f"⚠️ Error at point {idx}: {e}")
            results.append([lat, lon, None, None, None])

        time.sleep(1)  # 1 request/sec

    result = pd.DataFrame(results, columns=["lat","lon","matched_lat","matched_lon","road_name"])

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    result.to_csv(output_file, index=False)
    print(f"✅ Test reverse geocoding complete. Saved to {output_file}")

if __name__ == "__main__":
    reverse_geocode_single(df)
