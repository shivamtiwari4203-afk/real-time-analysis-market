# Indian Real Estate Market Analysis (Q3 2026)

A small Python project that reproduces the key tables and charts from the Indian real estate market report, using figures reported for Q3 2026 by Anarock, PropEquity, Knight Frank, JLL, Cushman & Wakefield and the RBI.

Position: November 2026. For information only; not investment advice.

## What it does

- Compares Q3 2026 housing sales across three trackers (they cover different city sets, so they are shown separately, not blended).
- Calculates residential supply and demand metrics: year-on-year changes, launch-to-sales ratio, and approximate months of inventory.
- Tracks unsold inventory by quarter, with quarter-on-quarter change.
- Summarises Jan–Sep 2026 office leasing across four trackers.
- Estimates the EMI impact of further RBI rate hikes on a home loan.
- Summarises the size of the listed REIT market.
- Saves six PNG charts.

## Requirements

- Python 3.9 or newer
- `pandas`
- `matplotlib`

```bash
pip install pandas matplotlib
```

## Run

```bash
python india_real_estate_analysis.py
```

The script prints the tables to the console and saves charts to a `charts/` folder:

| File | Shows |
|---|---|
| `01_trackers_yoy.png` | Q3 2026 sales growth by tracker |
| `02_unsold_inventory.png` | Unsold inventory, top 7 cities |
| `03_supply_vs_demand.png` | Launches vs sales, Q3 2025 and Q3 2026 |
| `04_office_leasing.png` | Jan–Sep 2026 office leasing by tracker |
| `05_repo_rate.png` | RBI repo rate path around the October 2026 hike |
| `06_reits.png` | Listed REIT assets and market capitalisation |

## Updating the data

All inputs sit in the `DATA` section at the top of `india_real_estate_analysis.py`. Edit the values there and re-run to refresh the output.

To change the EMI scenario, call `rate_hike_impact()` with different arguments (principal, years, base rate, size of each hike):

```python
rate_hike_impact(principal=7_500_000, years=25, base=8.0, hike_bps=25)
```

## Headline results

- Anarock: sales up 3% year on year, launches up 18%, unsold stock up 12% to about 630,590 homes.
- PropEquity shows sales down 6% and Knight Frank down 1%, depending on city coverage.
- Launch-to-sales ratio is about 1.14; unsold stock is roughly 19 months of current sales.
- RBI repo rate is 5.50% after the 7 October 2026 hike. Each further 25 bps adds about ₹775 a month to the EMI on a ₹50 lakh, 20-year loan at an assumed 7.75%.

## Caveats

- Figures come from consultancy reports as covered in the business press, not from the original reports.
- Trackers differ in city coverage and methodology; compare direction, not exact levels.
- "Months of inventory" is a simple estimate (unsold stock divided by current monthly sales), not a published statistic.
- The 7.75% EMI base rate is illustrative, not a surveyed lender rate.
- The repo rate series in the chart contains only the policy points used here, not a full history.

## Related files

- `Indian_Real_Estate_Market_Analysis.docx`: the full written report with sources.
- A slide deck covering the same topic.
