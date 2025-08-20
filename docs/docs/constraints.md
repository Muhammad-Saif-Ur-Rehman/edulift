# Ride Matching & Optimization Constraints

This document specifies the **hard** and **soft** constraints used by the Edulift ride‑matching system and the evaluation criteria defined in T7.

---

## 1) Entities and Notation

- **Requests**: pickup (origin, time window), dropoff (destination, deadline)
- **Vehicles**: capacity \(C\), start/end depots (optional)
- **Graph**: travel times/distances between points (from map‑matched data)

---

## 2) Hard Constraints

1. **Time Windows**
   - Pickup must occur within \([t_{\text{req}} - \Delta^- ,\, t_{\text{req}} + \Delta^+]\).
   - Dropoff must be at least **δ** minutes before event start (class).
   - Config: `time.pickup_window_min_before`, `time.pickup_window_max_after`, `time.dropoff_before_event_min`.

2. **Wait Time**
   - Rider wait at pickup ≤ `time.max_wait_min`.

3. **Ride Duration**
   - In‑vehicle time ≤ `time.max_ride_min`.

4. **Detour**
   - \(\frac{\text{shared\_time} - \text{solo\_time}}{\text{solo\_time}} \le \text{time.max\_detour\_ratio}\).
   - At night, use stricter `safety.night_match_max_detour`.

5. **Capacity**
   - Sum of riders on board at any time ≤ `capacity.vehicle_capacity`.
   - Optional wheelchair/luggage constraints if configured.

6. **Service Area & No‑Go Segments**
   - Pickup/dropoff must lie within service polygon (if provided).
   - Avoid roads in `safety.forbidden_roads`.

7. **Speed & Safety Checks**
   - Trips averaging > `safety.speed_kmh_max` are flagged (QC, not solver).

---

## 3) Soft Constraints (Objective)

Minimize:
\[
\alpha \cdot \text{TotalTravelTime} \;+\; 
\beta \cdot \text{TotalWaitTime} \;+\;
\gamma \cdot \text{UnmatchedTrips} \;+\;
\lambda \cdot \text{LatenessPenalty} \;+\;
\mu \cdot \text{CarbonCost}
\]

Weights are in `optimization.objective.weights`. Carbon cost is a proxy via distance/occupancy.

---

## 4) OR‑Tools Formulation (VRPTW + Capacity)

- **Variables**
  - Vehicle routes with time dimension (pickup → dropoff with precedence).
  - Load dimension for onboard passengers (capacity).
  - Optional: binary matching variables for pairing requests.

- **Dimensions**
  - **Time dimension** with per‑node windows (pickup window, dropoff deadline).
  - **Capacity dimension** with per‑arc increments/decrements at pickup/dropoff.

- **Constraints**
  - Precedence: pickup precedes corresponding dropoff.
  - Time windows & capacity as above.

- **Search**
  - `PATH_CHEAPEST_ARC` → `GUIDED_LOCAL_SEARCH`, time limit from config.

---

## 5) Safety Rules

- Night hours (`safety.night_hours`) apply stricter detours and optional rules (e.g., only pool with same‑sex riders if org policy requires — not enforced here by default).
- Respect forbidden roads and depots if given.
- Enforce minimum age for pooling (`safety.require_two_riders_min_age`).

---

## 6) Privacy & Ethics

- Remove PII; replace IDs with **salted hashes** (env var: `privacy.hash_id_salt_env`).
- **Coordinate rounding** to 5 decimals (~1.1 m). For public release, consider 4 decimals (~11 m).
- **Time rounding** to `privacy.time_bin_minutes` for logs.
- Do not release exact home/work inferences; publish only **cluster centroids**.
- Retain raw data privately; share only **processed** / **aggregated** datasets.

---

## 7) Configuration

All numeric thresholds live in `config/constraints.yaml`. Code should not hard‑code policy.
