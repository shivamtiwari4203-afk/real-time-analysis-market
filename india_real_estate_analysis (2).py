"""
Indian real estate market analysis, November 2026.

Reproduces the key tables and charts from the Word report using figures
reported for Q3 2026 (Anarock, PropEquity, Knight Frank, JLL, Cushman &
Wakefield, RBI). Edit the DATA section to update with new quarters.

Requires: pandas, matplotlib
Run:      python india_real_estate_analysis.py
Output:   printed summary + PNG charts in ./charts
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

OUT = Path("charts")
OUT.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# DATA (units are homes unless stated; source in comments)
# ----------------------------------------------------------------------------

# Residential Q3 2026 by tracker. Coverage differs, so do not blend them.
trackers = pd.DataFrame(
    {
        "tracker": ["Anarock", "PropEquity", "Knight Frank"],
        "coverage": ["Top 7 cities", "Top 9 cities", "Top 8 cities"],
        "q3_2026_sales": [100_220, 103_170, 86_767],
        "yoy_pct": [3, -6, -1],
    }
)

# Anarock unsold inventory, top 7 cities, quarter-end
inventory = pd.DataFrame(
    {
        "quarter": ["Q3 25", "Q4 25", "Q1 26", "Q2 26", "Q3 26"],
        "unsold": [561_750, 576_600, 601_210, 616_500, 630_590],
    }
)

# Anarock Q3 2026 supply/demand and price
anarock_q3 = {
    "sales_q3_2025": 97_080,
    "sales_q3_2026": 100_220,
    "launches_q3_2025": 96_690,
    "launches_q3_2026": 114_320,
    "inventory_q3_2025": 561_760,
    "inventory_q3_2026": 630_590,
    "avg_price_psf_2026": 9_714,  # INR per sq ft, +7% YoY
    "sales_value_cr_2025": 152_000,  # INR crore
    "sales_value_cr_2026": 155_000,
}

# Office leasing, Jan-Sep 2026 (million sq ft). Definitions differ by source.
office = pd.DataFrame(
    {
        "source": ["JLL (top 7)", "Cushman & Wakefield (top 8)", "Vestian", "Colliers (top 7, Grade A)"],
        "q3_2026_msf": [23.17, 22.0, 23.7, 18.7],
        "nine_month_msf": [61.06, 64.6, 65.0, 54.4],
    }
)

# Repo rate path (percent) around the October 2026 hike
repo = pd.DataFrame(
    {
        "date": ["Jun 2025", "Dec 2025", "Feb 2026", "Apr 2026", "Jun 2026", "Aug 2026", "Oct 2026"],
        "repo_pct": [5.50, 5.25, 5.25, 5.25, 5.25, 5.25, 5.50],
    }
)

# REITs (INR lakh crore)
reits = pd.DataFrame(
    {
        "period": ["Mar 2026 (FY26)", "Jun 2026 (Q1 FY27)"],
        "gross_assets": [2.72, 3.17],
        "market_cap": [1.70, 2.17],
    }
)


# ----------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------
def pct_change(new: float, old: float) -> float:
    return (new / old - 1) * 100


def residential_summary() -> pd.Series:
    a = anarock_q3
    launches_minus_sales = a["launches_q3_2026"] - a["sales_q3_2026"]
    return pd.Series(
        {
            "Sales YoY %": pct_change(a["sales_q3_2026"], a["sales_q3_2025"]),
            "Launches YoY %": pct_change(a["launches_q3_2026"], a["launches_q3_2025"]),
            "Unsold stock YoY %": pct_change(a["inventory_q3_2026"], a["inventory_q3_2025"]),
            "Sales value YoY %": pct_change(a["sales_value_cr_2026"], a["sales_value_cr_2025"]),
            "Launches minus sales (Q3 2026)": launches_minus_sales,
            "Launch-to-sales ratio": a["launches_q3_2026"] / a["sales_q3_2026"],
            # Rough: unsold stock divided by this quarter's monthly sales rate
            "Months of inventory (approx.)": a["inventory_q3_2026"] / (a["sales_q3_2026"] / 3),
            "Avg ticket INR crore (value/units)": a["sales_value_cr_2026"] / a["sales_q3_2026"],
        }
    ).round(2)


def inventory_trend() -> pd.DataFrame:
    df = inventory.copy()
    df["qoq_pct"] = df["unsold"].pct_change().mul(100).round(1)
    return df


def emi(principal: float, annual_rate_pct: float, years: int) -> float:
    """Monthly EMI for a floating-rate home loan."""
    r = annual_rate_pct / 12 / 100
    n = years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def rate_hike_impact(principal=5_000_000, years=20, base=7.75, hike_bps=25, hikes=(1, 2, 3)) -> pd.DataFrame:
    """EMI impact of cumulative 25 bps hikes. Base rate is an illustrative lender rate."""
    rows = [{"scenario": f"Today ({base:.2f}%)", "rate_pct": base, "emi": emi(principal, base, years)}]
    for k in hikes:
        rate = base + k * hike_bps / 100
        rows.append({"scenario": f"+{k * hike_bps} bps ({rate:.2f}%)", "rate_pct": rate, "emi": emi(principal, rate, years)})
    df = pd.DataFrame(rows)
    df["extra_per_month"] = (df["emi"] - df.loc[0, "emi"]).round(0)
    df["extra_total_over_loan"] = (df["extra_per_month"] * years * 12).round(0)
    df["emi"] = df["emi"].round(0)
    return df


# ----------------------------------------------------------------------------
# CHARTS
# ----------------------------------------------------------------------------
NAVY, BLUE, GREY = "#1F3A5F", "#2E5C8A", "#9AA5B1"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150)
    plt.close(fig)


def chart_trackers():
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = [BLUE if v >= 0 else "#C0504D" for v in trackers["yoy_pct"]]
    ax.bar(trackers["tracker"] + "\n" + trackers["coverage"], trackers["yoy_pct"], color=colors)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Q3 2026 sales, YoY %")
    ax.set_title("Same quarter, different answers: housing sales by tracker")
    for i, v in enumerate(trackers["yoy_pct"]):
        ax.text(i, v + (0.3 if v >= 0 else -0.8), f"{v:+d}%", ha="center")
    save(fig, "01_trackers_yoy.png")


def chart_inventory():
    df = inventory_trend()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df["quarter"], df["unsold"] / 1000, marker="o", color=NAVY)
    ax.set_ylabel("Unsold homes (thousand)")
    ax.set_title("Unsold inventory, top 7 cities (Anarock)")
    for x, y in zip(df["quarter"], df["unsold"] / 1000):
        ax.annotate(f"{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")
    ax.set_ylim(540, 650)
    save(fig, "02_unsold_inventory.png")


def chart_supply_demand():
    a = anarock_q3
    labels = ["Sales", "Launches"]
    q3_25 = [a["sales_q3_2025"], a["launches_q3_2025"]]
    q3_26 = [a["sales_q3_2026"], a["launches_q3_2026"]]
    x = range(2)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([i - 0.2 for i in x], [v / 1000 for v in q3_25], 0.4, label="Q3 2025", color=GREY)
    ax.bar([i + 0.2 for i in x], [v / 1000 for v in q3_26], 0.4, label="Q3 2026", color=NAVY)
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Units (thousand)")
    ax.set_title("Launches are outpacing sales (top 7, Anarock)")
    ax.legend()
    save(fig, "03_supply_vs_demand.png")


def chart_office():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(office["source"], office["nine_month_msf"], color=BLUE)
    ax.set_xlabel("Jan-Sep 2026 leasing / absorption (msf)")
    ax.set_title("Office leasing: record nine months across trackers")
    ax.invert_yaxis()
    for i, v in enumerate(office["nine_month_msf"]):
        ax.text(v + 0.5, i, f"{v:.1f}", va="center")
    save(fig, "04_office_leasing.png")


def chart_repo():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.step(repo["date"], repo["repo_pct"], where="post", color=NAVY, marker="o")
    ax.set_ylim(5.0, 5.75)
    ax.set_ylabel("Repo rate, %")
    ax.set_title("RBI repo rate: first hike since Feb 2023 (Oct 2026)")
    ax.annotate("+25 bps\ncalibrated tightening", ("Oct 2026", 5.50), textcoords="offset points", xytext=(-90, -30))
    save(fig, "05_repo_rate.png")


def chart_reits():
    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(reits))
    ax.bar([i - 0.2 for i in x], reits["gross_assets"], 0.4, label="Gross assets", color=NAVY)
    ax.bar([i + 0.2 for i in x], reits["market_cap"], 0.4, label="Market cap", color=BLUE)
    ax.set_xticks(list(x), reits["period"])
    ax.set_ylabel("INR lakh crore")
    ax.set_title("Listed REITs in India")
    ax.legend()
    save(fig, "06_reits.png")


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main():
    pd.set_option("display.width", 120)
    print("\n=== Q3 2026 sales by tracker ===")
    print(trackers.to_string(index=False))

    print("\n=== Residential supply/demand (Anarock, top 7) ===")
    print(residential_summary().to_string())

    print("\n=== Unsold inventory trend ===")
    print(inventory_trend().to_string(index=False))

    print("\n=== Office leasing (msf) ===")
    print(office.to_string(index=False))
    print(f"Average of nine-month figures: {office['nine_month_msf'].mean():.1f} msf")

    print("\n=== EMI impact of further hikes: INR 50 lakh, 20 years ===")
    print(rate_hike_impact().to_string(index=False))

    print("\n=== REITs ===")
    print(reits.to_string(index=False))
    growth = pct_change(reits["gross_assets"].iloc[-1], reits["gross_assets"].iloc[0])
    print(f"Gross assets growth Mar-Jun 2026: {growth:.1f}%")

    for fn in (chart_trackers, chart_inventory, chart_supply_demand, chart_office, chart_repo, chart_reits):
        fn()
    print(f"\nCharts saved to {OUT.resolve()}")


if __name__ == "__main__":
    main()
