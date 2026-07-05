"""
Retail Business Performance & Profitability Analysis
------------------------------------------------------
Performs data cleaning, EDA, and correlation analysis on the Superstore
dataset, and saves all charts used in the dashboard / report.

Run:  python scripts/analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

# ---------------------------------------------------------------
# 1. LOAD & CLEAN DATA
# ---------------------------------------------------------------
df = pd.read_csv("data/Superstore.csv", encoding="latin1")
df.columns = [c.strip() for c in df.columns]

# Parse dates
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")

# Drop exact duplicate rows, if any
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# Confirm no nulls (already validated, but keep this defensive)
df = df.dropna(subset=["Sales", "Profit", "Category", "Sub-Category", "Region"])

# Derived columns
df["Profit Margin"] = df["Profit"] / df["Sales"]
df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Order Year"] = df["Order Date"].dt.year
df["Season"] = df["Order Date"].dt.month % 12 // 3 + 1
season_map = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
df["Season"] = df["Season"].map(season_map)

print(f"Final dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------
# 2. PROFIT MARGIN BY CATEGORY / SUB-CATEGORY
# ---------------------------------------------------------------
cat_summary = (
    df.groupby("Category")
    .agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"))
    .assign(margin_pct=lambda x: x.total_profit / x.total_sales * 100)
    .sort_values("margin_pct", ascending=False)
)
cat_summary.to_csv("data/category_summary.csv")
print("\nCategory summary:\n", cat_summary)

subcat_summary = (
    df.groupby(["Category", "Sub-Category"])
    .agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"))
    .assign(margin_pct=lambda x: x.total_profit / x.total_sales * 100)
    .sort_values("margin_pct")
)
subcat_summary.to_csv("data/subcategory_summary.csv")

# Chart: Sub-category profit margin (sorted, color-coded by profit/loss)
plt.figure(figsize=(10, 7))
sc = subcat_summary.reset_index().sort_values("margin_pct")
colors = ["#d62728" if v < 0 else "#2ca02c" for v in sc["margin_pct"]]
plt.barh(sc["Sub-Category"], sc["margin_pct"], color=colors)
plt.axvline(0, color="black", linewidth=0.8)
plt.title("Profit Margin (%) by Sub-Category")
plt.xlabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("images/subcategory_margin.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 3. CORRELATION: SHIPPING DAYS (inventory-lag proxy) vs PROFITABILITY
# ---------------------------------------------------------------
ship_corr = df[["Shipping Days", "Profit Margin", "Discount", "Sales", "Profit"]].corr()
ship_corr.to_csv("data/correlation_matrix.csv")
print("\nCorrelation matrix:\n", ship_corr.round(3))

plt.figure(figsize=(6, 5))
sns.heatmap(ship_corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Correlation Matrix: Shipping Days, Discount, Sales & Profit")
plt.tight_layout()
plt.savefig("images/correlation_heatmap.png", dpi=150)
plt.close()

# Shipping days by sub-category vs margin
ship_by_subcat = (
    df.groupby("Sub-Category")
    .agg(avg_shipping_days=("Shipping Days", "mean"), margin_pct=("Profit Margin", "mean"))
    .assign(margin_pct=lambda x: x.margin_pct * 100)
)
ship_by_subcat.to_csv("data/shipping_vs_margin.csv")

# ---------------------------------------------------------------
# 4. REGIONAL & SEASONAL ANALYSIS
# ---------------------------------------------------------------
region_summary = (
    df.groupby("Region")
    .agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"))
    .assign(margin_pct=lambda x: x.total_profit / x.total_sales * 100)
    .sort_values("total_profit", ascending=False)
)
region_summary.to_csv("data/region_summary.csv")

plt.figure(figsize=(8, 5))
sns.barplot(x=region_summary.index, y=region_summary["total_profit"], palette="crest")
plt.title("Total Profit by Region")
plt.ylabel("Total Profit ($)")
plt.tight_layout()
plt.savefig("images/region_profit.png", dpi=150)
plt.close()

season_summary = (
    df.groupby("Season")
    .agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"))
    .reindex(["Winter", "Spring", "Summer", "Fall"])
)
season_summary.to_csv("data/season_summary.csv")

plt.figure(figsize=(8, 5))
x = np.arange(len(season_summary))
width = 0.35
plt.bar(x - width / 2, season_summary["total_sales"], width, label="Sales")
plt.bar(x + width / 2, season_summary["total_profit"], width, label="Profit")
plt.xticks(x, season_summary.index)
plt.title("Seasonal Sales vs Profit")
plt.legend()
plt.tight_layout()
plt.savefig("images/seasonal_sales_profit.png", dpi=150)
plt.close()

# Monthly trend
monthly = df.groupby("Order Month").agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"))
monthly.to_csv("data/monthly_trend.csv")

plt.figure(figsize=(12, 5))
plt.plot(monthly.index, monthly["total_sales"], marker="o", label="Sales")
plt.plot(monthly.index, monthly["total_profit"], marker="o", label="Profit")
plt.xticks(rotation=75, fontsize=8)
plt.title("Monthly Sales & Profit Trend")
plt.legend()
plt.tight_layout()
plt.savefig("images/monthly_trend.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 5. DISCOUNT IMPACT
# ---------------------------------------------------------------
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Discount", y="Profit Margin", hue="Category", alpha=0.5)
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Discount vs Profit Margin")
plt.tight_layout()
plt.savefig("images/discount_vs_margin.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 6. SLOW-MOVING / OVERSTOCKED ITEM SIGNAL
# (proxy: low quantity sold + long shipping days + negative margin)
# ---------------------------------------------------------------
product_signal = (
    df.groupby(["Category", "Sub-Category"])
    .agg(
        avg_shipping_days=("Shipping Days", "mean"),
        total_quantity=("Quantity", "sum"),
        margin_pct=("Profit Margin", "mean"),
    )
    .assign(margin_pct=lambda x: x.margin_pct * 100)
    .sort_values("margin_pct")
)
product_signal.to_csv("data/slow_moving_signal.csv")

print("\nAll charts saved to images/. All summary tables saved to data/.")
print("Done.")
