#!/usr/bin/env python3
"""
generate_climate_grid.py
------------------------
Generates assets/data/climate-grid.json for the Flomads sit-scouting tool.

Queries Open-Meteo's free climate API (no key required) for each country
centroid and retrieves monthly average temperature and precipitation normals
(1991-2020 climatology).

Output structure:
{
  "meta": { "generated": "...", "source": "...", "months": [...] },
  "countries": {
    "GB": {
      "name": "United Kingdom",
      "lat": 55.38,
      "lon": -3.44,
      "monthly": {
        "temp_max": [6.2, 7.1, ...],   // avg daily high °C, index 0=Jan
        "temp_min": [1.8, 2.1, ...],   // avg daily low °C
        "temp_mean": [4.0, 4.6, ...],  // avg mean °C
        "precip":   [72, 55, ...]      // avg monthly precip mm
      }
    },
    ...
  }
}

Usage:
    pip install requests
    python3 generate_climate_grid.py
    # Writes climate-grid.json in the current directory.
    # Move it to assets/data/ in your Jekyll site.
"""

import json
import time
import sys
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Country centroids — ISO 3166-1 alpha-2, name, lat, lon
# ---------------------------------------------------------------------------
COUNTRIES = [
    ("AF", "Afghanistan", 33.93, 67.71),
    ("AL", "Albania", 41.15, 20.17),
    ("DZ", "Algeria", 28.03, 1.66),
    ("AO", "Angola", -11.20, 17.87),
    ("AR", "Argentina", -38.42, -63.62),
    ("AM", "Armenia", 40.07, 45.04),
    ("AU", "Australia", -25.27, 133.78),
    ("AT", "Austria", 47.52, 14.55),
    ("AZ", "Azerbaijan", 40.14, 47.58),
    ("BS", "Bahamas", 25.03, -77.40),
    ("BH", "Bahrain", 26.02, 50.55),
    ("BD", "Bangladesh", 23.68, 90.35),
    ("BY", "Belarus", 53.71, 27.95),
    ("BE", "Belgium", 50.50, 4.47),
    ("BZ", "Belize", 17.19, -88.50),
    ("BJ", "Benin", 9.31, 2.32),
    ("BT", "Bhutan", 27.51, 90.43),
    ("BO", "Bolivia", -16.29, -63.59),
    ("BA", "Bosnia and Herzegovina", 43.92, 17.68),
    ("BW", "Botswana", -22.33, 24.68),
    ("BR", "Brazil", -14.24, -51.93),
    ("BN", "Brunei", 4.54, 114.73),
    ("BG", "Bulgaria", 42.73, 25.49),
    ("BF", "Burkina Faso", 12.36, -1.53),
    ("BI", "Burundi", -3.37, 29.92),
    ("CV", "Cape Verde", 16.54, -23.04),
    ("KH", "Cambodia", 12.57, 104.99),
    ("CM", "Cameroon", 3.85, 11.50),
    ("CA", "Canada", 56.13, -106.35),
    ("CF", "Central African Republic", 6.61, 20.94),
    ("TD", "Chad", 15.45, 18.73),
    ("CL", "Chile", -35.68, -71.54),
    ("CN", "China", 35.86, 104.19),
    ("CO", "Colombia", 4.57, -74.30),
    ("KM", "Comoros", -11.64, 43.33),
    ("CD", "Congo (DRC)", -4.04, 21.76),
    ("CG", "Congo (Republic)", -0.23, 15.83),
    ("CR", "Costa Rica", 9.75, -83.75),
    ("HR", "Croatia", 45.10, 15.20),
    ("CU", "Cuba", 21.52, -77.78),
    ("CY", "Cyprus", 35.13, 33.43),
    ("CZ", "Czech Republic", 49.82, 15.47),
    ("DK", "Denmark", 56.26, 9.50),
    ("DJ", "Djibouti", 11.83, 42.59),
    ("DO", "Dominican Republic", 18.74, -70.16),
    ("EC", "Ecuador", -1.83, -78.18),
    ("EG", "Egypt", 26.82, 30.80),
    ("SV", "El Salvador", 13.79, -88.90),
    ("GQ", "Equatorial Guinea", 1.65, 10.27),
    ("ER", "Eritrea", 15.18, 39.78),
    ("EE", "Estonia", 58.60, 25.01),
    ("SZ", "Eswatini", -26.52, 31.47),
    ("ET", "Ethiopia", 9.15, 40.49),
    ("FJ", "Fiji", -16.58, 179.41),
    ("FI", "Finland", 61.92, 25.75),
    ("FR", "France", 46.23, 2.21),
    ("GA", "Gabon", -0.80, 11.61),
    ("GM", "Gambia", 13.44, -15.31),
    ("GE", "Georgia", 42.32, 43.36),
    ("DE", "Germany", 51.17, 10.45),
    ("GH", "Ghana", 7.95, -1.02),
    ("GR", "Greece", 39.07, 21.82),
    ("GT", "Guatemala", 15.78, -90.23),
    ("GN", "Guinea", 9.95, -11.24),
    ("GW", "Guinea-Bissau", 11.80, -15.18),
    ("GY", "Guyana", 4.86, -58.93),
    ("HT", "Haiti", 18.97, -72.29),
    ("HN", "Honduras", 15.20, -86.24),
    ("HU", "Hungary", 47.16, 19.50),
    ("IS", "Iceland", 64.96, -19.02),
    ("IN", "India", 20.59, 78.96),
    ("ID", "Indonesia", -0.79, 113.92),
    ("IR", "Iran", 32.43, 53.69),
    ("IQ", "Iraq", 33.22, 43.68),
    ("IE", "Ireland", 53.41, -8.24),
    ("IL", "Israel", 31.05, 34.85),
    ("IT", "Italy", 41.87, 12.57),
    ("JM", "Jamaica", 18.11, -77.30),
    ("JP", "Japan", 36.20, 138.25),
    ("JO", "Jordan", 30.59, 36.24),
    ("KZ", "Kazakhstan", 48.02, 66.92),
    ("KE", "Kenya", -0.02, 37.91),
    ("KW", "Kuwait", 29.31, 47.48),
    ("KG", "Kyrgyzstan", 41.20, 74.77),
    ("LA", "Laos", 19.86, 102.50),
    ("LV", "Latvia", 56.88, 24.60),
    ("LB", "Lebanon", 33.85, 35.86),
    ("LS", "Lesotho", -29.61, 28.23),
    ("LR", "Liberia", 6.43, -9.43),
    ("LY", "Libya", 26.34, 17.23),
    ("LT", "Lithuania", 55.17, 23.88),
    ("LU", "Luxembourg", 49.82, 6.13),
    ("MG", "Madagascar", -18.77, 46.87),
    ("MW", "Malawi", -13.25, 34.30),
    ("MY", "Malaysia", 4.21, 108.96),
    ("MV", "Maldives", 3.20, 73.22),
    ("ML", "Mali", 17.57, -3.99),
    ("MT", "Malta", 35.94, 14.38),
    ("MR", "Mauritania", 21.01, -10.94),
    ("MX", "Mexico", 23.63, -102.55),
    ("MD", "Moldova", 47.41, 28.37),
    ("MN", "Mongolia", 46.86, 103.85),
    ("ME", "Montenegro", 42.71, 19.37),
    ("MA", "Morocco", 31.79, -7.09),
    ("MZ", "Mozambique", -18.67, 35.53),
    ("MM", "Myanmar", 19.17, 96.66),
    ("NA", "Namibia", -22.96, 18.49),
    ("NP", "Nepal", 28.39, 84.12),
    ("NL", "Netherlands", 52.13, 5.29),
    ("NZ", "New Zealand", -40.90, 174.89),
    ("NI", "Nicaragua", 12.87, -85.21),
    ("NE", "Niger", 17.61, 8.08),
    ("NG", "Nigeria", 9.08, 8.68),
    ("MK", "North Macedonia", 41.61, 21.75),
    ("NO", "Norway", 60.47, 8.47),
    ("OM", "Oman", 21.51, 55.92),
    ("PK", "Pakistan", 30.38, 69.35),
    ("PA", "Panama", 8.54, -80.78),
    ("PG", "Papua New Guinea", -6.31, 143.96),
    ("PY", "Paraguay", -23.44, -58.44),
    ("PE", "Peru", -9.19, -75.02),
    ("PH", "Philippines", 12.88, 121.77),
    ("PL", "Poland", 51.92, 19.15),
    ("PT", "Portugal", 39.40, -8.22),
    ("QA", "Qatar", 25.35, 51.18),
    ("RO", "Romania", 45.94, 24.97),
    ("RU", "Russia", 61.52, 105.32),
    ("RW", "Rwanda", -1.94, 29.87),
    ("SA", "Saudi Arabia", 23.89, 45.08),
    ("SN", "Senegal", 14.50, -14.45),
    ("RS", "Serbia", 44.02, 21.01),
    ("SL", "Sierra Leone", 8.46, -11.78),
    ("SK", "Slovakia", 48.67, 19.70),
    ("SI", "Slovenia", 46.15, 14.99),
    ("SO", "Somalia", 5.15, 46.20),
    ("ZA", "South Africa", -30.56, 22.94),
    ("SS", "South Sudan", 7.86, 29.69),
    ("ES", "Spain", 40.46, -3.75),
    ("LK", "Sri Lanka", 7.87, 80.77),
    ("SD", "Sudan", 12.86, 30.22),
    ("SR", "Suriname", 3.92, -56.03),
    ("SE", "Sweden", 60.13, 18.64),
    ("CH", "Switzerland", 46.82, 8.23),
    ("SY", "Syria", 34.80, 38.99),
    ("TW", "Taiwan", 23.70, 121.00),
    ("TJ", "Tajikistan", 38.86, 71.28),
    ("TZ", "Tanzania", -6.37, 34.89),
    ("TH", "Thailand", 15.87, 100.99),
    ("TL", "Timor-Leste", -8.87, 125.73),
    ("TG", "Togo", 8.62, 0.82),
    ("TT", "Trinidad and Tobago", 10.69, -61.22),
    ("TN", "Tunisia", 33.89, 9.54),
    ("TR", "Turkey", 38.96, 35.24),
    ("TM", "Turkmenistan", 38.97, 59.56),
    ("UG", "Uganda", 1.37, 32.29),
    ("UA", "Ukraine", 48.38, 31.17),
    ("AE", "United Arab Emirates", 23.42, 53.85),
    ("GB", "United Kingdom", 55.38, -3.44),
    ("US", "United States", 37.09, -95.71),
    ("UY", "Uruguay", -32.52, -55.77),
    ("UZ", "Uzbekistan", 41.38, 64.59),
    ("VE", "Venezuela", 6.42, -66.59),
    ("VN", "Vietnam", 14.06, 108.28),
    ("YE", "Yemen", 15.55, 48.52),
    ("ZM", "Zambia", -13.13, 27.85),
    ("ZW", "Zimbabwe", -19.02, 29.15),
]

# ---------------------------------------------------------------------------
# Open-Meteo climate API — 1991-2020 ERA5 monthly normals
# ---------------------------------------------------------------------------
BASE_URL = "https://climate-api.open-meteo.com/v1/climate"

PARAMS = {
    "start_date": "1991-01-01",
    "end_date": "2020-12-31",
    "models": "ERA5",
    "monthly": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum",
    "timezone": "UTC",
}

MONTH_NAMES = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]


def fetch_climate(iso, name, lat, lon):
    """Fetch 30-year monthly climate normals for one coordinate."""
    params = {**PARAMS, "latitude": lat, "longitude": lon}
    try:
        r = requests.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  ERROR fetching {iso} ({name}): {e}")
        return None

    monthly = data.get("monthly", {})
    if not monthly or "time" not in monthly:
        print(f"  WARN: no monthly data for {iso}")
        return None

    # Aggregate 30 years of monthly values into per-month averages (index 0=Jan)
    t_max  = [[] for _ in range(12)]
    t_min  = [[] for _ in range(12)]
    t_mean = [[] for _ in range(12)]
    precip = [[] for _ in range(12)]

    for i, ts in enumerate(monthly["time"]):
        # ts is "YYYY-MM" or "YYYY-MM-DD"
        month_idx = int(ts[5:7]) - 1
        def safe(key, i=i):
            val = monthly.get(key, [None]*9999)
            return val[i] if i < len(val) else None

        mx = safe("temperature_2m_max")
        mn = safe("temperature_2m_min")
        me = safe("temperature_2m_mean")
        pr = safe("precipitation_sum")

        if mx is not None: t_max[month_idx].append(mx)
        if mn is not None: t_min[month_idx].append(mn)
        if me is not None: t_mean[month_idx].append(me)
        if pr is not None: precip[month_idx].append(pr)

    def avg(lst):
        return round(sum(lst) / len(lst), 1) if lst else None

    return {
        "temp_max":  [avg(t_max[m])  for m in range(12)],
        "temp_min":  [avg(t_min[m])  for m in range(12)],
        "temp_mean": [avg(t_mean[m]) for m in range(12)],
        "precip":    [avg(precip[m]) for m in range(12)],
    }


def main():
    output = {
        "meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "source": "Open-Meteo Climate API — ERA5 1991-2020 monthly normals",
            "months": MONTH_NAMES,
            "units": {
                "temp_max":  "°C average daily high",
                "temp_min":  "°C average daily low",
                "temp_mean": "°C average mean",
                "precip":    "mm total for month (averaged over 30 years)",
            },
            "note": "Index 0 = January, index 11 = December",
        },
        "countries": {}
    }

    total = len(COUNTRIES)
    failed = []

    for idx, (iso, name, lat, lon) in enumerate(COUNTRIES, 1):
        print(f"[{idx:3}/{total}] {iso}  {name}...", end=" ", flush=True)
        result = fetch_climate(iso, name, lat, lon)
        if result:
            output["countries"][iso] = {
                "name": name,
                "lat": lat,
                "lon": lon,
                "monthly": result,
            }
            print("✓")
        else:
            failed.append((iso, name))
            print("✗ skipped")

        # Polite delay — Open-Meteo free tier, no key required but be nice
        time.sleep(0.4)

    out_path = "climate-grid.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, separators=(",", ":"))  # compact, no whitespace

    size_kb = len(json.dumps(output)) / 1024
    print(f"\nDone. {len(output['countries'])} countries written to {out_path}")
    print(f"File size: ~{size_kb:.0f} KB")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        for iso, name in failed:
            print(f"  {iso}  {name}")


if __name__ == "__main__":
    main()