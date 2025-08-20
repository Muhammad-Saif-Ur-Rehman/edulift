# Dataset README

This repository contains the mobility data used for Edulift ride‑matching experiments.

## Structure

data/
raw/
ride_logs/ # Original ride/event logs (immutable)
gps_traces/ # Original GPS traces (immutable)
student_schedules/ # Sample schedules (if any)
processed/
eVED_171101_week_matched.csv # GPS + map-matched coords + road_name
features/
eVED_features.csv # Trip-level features (T5)
splits/
train.csv / val.csv / test.csv # Temporal splits (T7)

pgsql
Copy
Edit

## Lineage / Regeneration

1. **T3 (Preprocess)**
   - Clean GPS, normalize columns, remove bad records.
2. **T4 (Map‑Matching)**
   - Snap lat/lon to nearest road; enrich with `matched_lat`, `matched_lon`, optional `road_name`.
3. **T5 (Features)**
   - Trip stats: duration, distance, avg speed; OD clustering for starts/ends.
4. **T6 (EDA)**
   - Peak times / distributions / top routes / carbon baseline.
5. **T7 (Splits + Eval)**
   - Temporal 70/15/15 split and evaluation config.

> See `scripts/` for runnable steps and `config/constraints.yaml` for parameters.

## Schemas

### `processed/eVED_171101_week_matched.csv`

| Column        | Type    | Unit     | Notes                                  |
|---------------|---------|----------|----------------------------------------|
| VehId         | float   | –        | Vehicle identifier (anon)              |
| Trip          | float   | –        | Trip ID (anon)                         |
| timestamp     | string  | –        | Trip‑relative time (epoch baseline)    |
| lat, lon      | float   | deg      | Original GPS                           |
| matched_lat, matched_lon | float | deg | Map‑matched coordinates               |
| road_name     | string  | –        | Optional (may be null)                 |

### `features/eVED_features.csv` (T5 output)

| Column             | Type    | Unit | Notes                                          |
|--------------------|---------|------|------------------------------------------------|
| Trip               | float   | –    | Trip ID                                        |
| start_time         | datetime| –    | Relative datetime (not real clock)             |
| end_time           | datetime| –    | Relative datetime                              |
| duration_min       | float   | min  | Trip duration                                  |
| distance_km        | float   | km   | Haversine over matched coords                  |
| avg_speed_kmh      | float   | km/h | distance_km / (duration_min/60)                |
| matched_lat_start  | float   | deg  | Start point (matched)                          |
| matched_lon_start  | float   | deg  | Start point (matched)                          |
| od_cluster_start   | int     | –    | DBSCAN cluster ID (origin)                     |
| matched_lat_end    | float   | deg  | End point (matched)                            |
| matched_lon_end    | float   | deg  | End point (matched)                            |
| od_cluster_end     | int     | –    | DBSCAN cluster ID (destination)                |

### `splits/*.csv` (T7 output)

Same columns as features; sorted by `start_time` then sliced into train/val/test.

## Known Limitations

- `timestamp` is **trip‑relative** (epoch baseline), so peak‑hour charts use a fallback (duration buckets) unless a real date column is provided.
- `road_name` may be null where the map service didn’t return names; this does **not** affect optimization.

## Privacy

- IDs are anonymized; no PII stored.
- Coordinates rounded to 5 decimals by default.
- Public sharing should use **aggregated** outputs whenever possible.

## Reproducibility

- Track files with Git + DVC/Git‑LFS per repo guidelines.
- Keep `config/constraints.yaml` under version control; do not commit raw secrets.