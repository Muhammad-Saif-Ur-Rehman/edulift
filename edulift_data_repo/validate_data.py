import pandas as pd
import sys

features = "D:\\Heisen Corporation projects\\Project 4 - Edulift\\edulift-data-repo\\data\\processed\\eVED_features.csv"
df = pd.read_csv(features)

problems = []

if df["duration_min"].le(0).any():
    problems.append("Non‑positive durations found.")
if df["distance_km"].lt(0).any():
    problems.append("Negative distances found.")
if df["avg_speed_kmh"].gt(130).any():
    problems.append("Unrealistic avg speeds >130 km/h.")
if df[["matched_lat_start","matched_lon_start","matched_lat_end","matched_lon_end"]].isna().any().any():
    problems.append("Missing matched coordinates in start/end.")

print("✅ Validation passed." if not problems else "❌ Issues:\n- " + "\n- ".join(problems))
sys.exit(1 if problems else 0)

