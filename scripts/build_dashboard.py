"""
Builds an interactive HTML dashboard (Plotly) for the Retail Profitability
Analysis project. Acts as a portable substitute/companion for a Tableau
dashboard so the project can be viewed directly on GitHub Pages or any
browser without needing Tableau installed.

Run:  python scripts/build_dashboard.py
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

df = pd.read_csv("data/Superstore.csv", encoding="latin1")
df.columns = [c.strip() for c in df.columns]
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin"] = df["Profit"] / df["Sales"] * 100

# ---------------- KPI numbers ----------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
margin = total_profit / total_sales * 100
total_orders = df["Order ID"].nunique()

# ---------------- Chart 1: Profit margin by Sub-Category ----------------
subcat = (
    df.groupby(["Category", "Sub-Category"])
    .agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"))
    .reset_index()
)
subcat["margin_pct"] = subcat["total_profit"] / subcat["total_sales"] * 100
subcat = subcat.sort_values("margin_pct")
fig1 = px.bar(
    subcat, x="margin_pct", y="Sub-Category", color="margin_pct",
    color_continuous_scale=["#d62728", "#f7f7f7", "#2ca02c"],
    orientation="h", title="Profit Margin (%) by Sub-Category",
    labels={"margin_pct": "Profit Margin (%)"}
)
fig1.update_layout(coloraxis_showscale=False, height=520)

# ---------------- Chart 2: Region x Category profit (dropdown filter) ----------------
region_cat = df.groupby(["Region", "Category"]).agg(total_profit=("Profit", "sum")).reset_index()
fig2 = px.bar(
    region_cat, x="Region", y="total_profit", color="Category", barmode="group",
    title="Profit by Region & Category",
    labels={"total_profit": "Total Profit ($)"}
)
fig2.update_layout(height=480)

# ---------------- Chart 3: Monthly Sales & Profit trend ----------------
monthly = df.groupby("Order Month").agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum")).reset_index()
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=monthly["Order Month"], y=monthly["total_sales"], name="Sales", mode="lines+markers"))
fig3.add_trace(go.Scatter(x=monthly["Order Month"], y=monthly["total_profit"], name="Profit", mode="lines+markers"))
fig3.update_layout(title="Monthly Sales & Profit Trend", height=480, xaxis_tickangle=-60)

# ---------------- Chart 4: Discount vs Profit Margin ----------------
fig4 = px.scatter(
    df, x="Discount", y="Profit Margin", color="Category", opacity=0.5,
    title="Discount vs Profit Margin", labels={"Profit Margin": "Profit Margin (%)"}
)
fig4.add_hline(y=0, line_dash="dash", line_color="gray")
fig4.update_layout(height=480)

# ---------------- Chart 5: Region map-style bar (Sales vs Profit) ----------------
region_summary = df.groupby("Region").agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum")).reset_index()
fig5 = go.Figure()
fig5.add_trace(go.Bar(x=region_summary["Region"], y=region_summary["total_sales"], name="Sales"))
fig5.add_trace(go.Bar(x=region_summary["Region"], y=region_summary["total_profit"], name="Profit"))
fig5.update_layout(title="Regional Sales vs Profit", barmode="group", height=480)

# ---------------- Assemble single HTML page ----------------
configs = dict(displaylogo=False)
charts_html = {
    "fig1": pio.to_html(fig1, include_plotlyjs=False, full_html=False, config=configs),
    "fig2": pio.to_html(fig2, include_plotlyjs=False, full_html=False, config=configs),
    "fig3": pio.to_html(fig3, include_plotlyjs=False, full_html=False, config=configs),
    "fig4": pio.to_html(fig4, include_plotlyjs=False, full_html=False, config=configs),
    "fig5": pio.to_html(fig5, include_plotlyjs=False, full_html=False, config=configs),
}

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Retail Business Performance & Profitability Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  :root {{
    --bg: #0f1117;
    --panel: #171a23;
    --accent: #4f8cff;
    --green: #2ca02c;
    --red: #d62728;
    --text: #e8eaf0;
    --muted: #9aa0ad;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
  }}
  header {{
    padding: 28px 40px 10px 40px;
    border-bottom: 1px solid #262a35;
  }}
  header h1 {{
    margin: 0 0 4px 0;
    font-size: 26px;
    font-weight: 700;
  }}
  header p {{
    margin: 0;
    color: var(--muted);
    font-size: 14px;
  }}
  .kpi-row {{
    display: flex;
    gap: 18px;
    padding: 24px 40px;
    flex-wrap: wrap;
  }}
  .kpi-card {{
    background: var(--panel);
    border: 1px solid #262a35;
    border-radius: 12px;
    padding: 18px 22px;
    min-width: 200px;
    flex: 1;
  }}
  .kpi-card .label {{
    color: var(--muted);
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .kpi-card .value {{
    font-size: 28px;
    font-weight: 700;
    margin-top: 6px;
  }}
  .kpi-card .value.profit {{ color: var(--green); }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding: 0 40px 40px 40px;
  }}
  .full-width {{ grid-column: 1 / -1; }}
  .chart-card {{
    background: var(--panel);
    border: 1px solid #262a35;
    border-radius: 12px;
    padding: 10px;
  }}
  footer {{
    text-align: center;
    color: var(--muted);
    font-size: 12px;
    padding: 20px;
  }}
  @media (max-width: 900px) {{
    .grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header>
  <h1>Retail Business Performance & Profitability Dashboard</h1>
  <p>Superstore Dataset &middot; Sales, Profit & Margin Analysis Across Region, Category & Time</p>
</header>

<div class="kpi-row">
  <div class="kpi-card">
    <div class="label">Total Sales</div>
    <div class="value">${total_sales:,.0f}</div>
  </div>
  <div class="kpi-card">
    <div class="label">Total Profit</div>
    <div class="value profit">${total_profit:,.0f}</div>
  </div>
  <div class="kpi-card">
    <div class="label">Overall Profit Margin</div>
    <div class="value">{margin:.1f}%</div>
  </div>
  <div class="kpi-card">
    <div class="label">Total Orders</div>
    <div class="value">{total_orders:,}</div>
  </div>
</div>

<div class="grid">
  <div class="chart-card full-width">{charts_html['fig1']}</div>
  <div class="chart-card">{charts_html['fig2']}</div>
  <div class="chart-card">{charts_html['fig5']}</div>
  <div class="chart-card full-width">{charts_html['fig3']}</div>
  <div class="chart-card full-width">{charts_html['fig4']}</div>
</div>

<footer>Built with Python & Plotly &middot; Data: Sample Superstore Dataset (Kaggle)</footer>

</body>
</html>
"""

with open("dashboard/dashboard.html", "w") as f:
    f.write(html_template)

print("Dashboard written to dashboard/dashboard.html")
print(f"Total Sales: ${total_sales:,.0f} | Total Profit: ${total_profit:,.0f} | Margin: {margin:.1f}%")
