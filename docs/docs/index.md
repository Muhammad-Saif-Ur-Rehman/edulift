# EduLift Data Repo documentation!

## Description

Synthetic datasets for EduLift (ride logs, GPS traces, schedules)

## Commands

The Makefile contains the central entry points for common tasks related to this project.


# Data Schema — Cleaned GPS Traces

This document describes the schema and format of the cleaned GPS trace dataset (`gps_traces_clean.csv`) produced after preprocessing in **T3**.

---

## File Path
..data/processed/gps_traces_clean.csv


---

## Schema

| Column       | Type      | Description                                                                 |
|--------------|-----------|-----------------------------------------------------------------------------|
| drive_id     | Integer   | Unique trip or drive identifier (from original `DriveNo`).                  |
| timestamp    | Datetime  | GPS record timestamp in **UTC**, ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`).   |
| lon          | Float     | Longitude in decimal degrees, rounded to 6 decimal places.                  |
| lat          | Float     | Latitude in decimal degrees, rounded to 6 decimal places.                   |

---

## Data Characteristics
- **Coordinate Range:**  
  - Latitude: `-90.000000` to `90.000000`  
  - Longitude: `-180.000000` to `180.000000`
- **Time Zone:**  
  - All timestamps are converted to **UTC** regardless of original timezone.
- **Precision:**  
  - Coordinates are rounded to 6 decimal places (~0.11 meter accuracy).
- **Ordering:**  
  - Records are sorted by `drive_id` and then by `timestamp` in ascending order.

---

## Preprocessing Steps Applied
1. Renamed columns for consistency.
2. Converted timestamps to UTC ISO 8601 format.
3. Ensured latitude/longitude values are numeric and within valid ranges.
4. Removed records with missing or invalid values.
5. Removed unrealistic speed jumps (> 200 km/h) between consecutive points.
6. Dropped temporary calculation columns from the final file.

---

## Usage Notes
- This dataset is ready for:
  - **Map-matching** (T4)
  - **Feature engineering** (T5)
  - **Exploratory data analysis** (T6)
- Original raw dataset is stored separately in:

..data/raw/gps_traces/taxi_data_subset.csv

and can be reprocessed if needed.
