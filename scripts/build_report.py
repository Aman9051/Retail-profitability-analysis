"""
Generates the 1-2 page PDF project report required by the internship
guidelines: Introduction, Abstract, Tools Used, Steps Involved, Conclusion.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontSize=9.5, leading=13, alignment=TA_JUSTIFY, spaceAfter=6))
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontSize=15, spaceAfter=4, textColor=colors.HexColor("#1a2744")))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontSize=11.5, spaceBefore=8, spaceAfter=3, textColor=colors.HexColor("#2255aa")))
styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=8.5, leading=11, textColor=colors.HexColor("#555555")))

story = []

# ---- Title block ----
story.append(Paragraph("Retail Business Performance &amp; Profitability Analysis", styles["H1"]))
story.append(Spacer(1, 10))

# ---- Abstract ----
story.append(Paragraph("Abstract", styles["H2"]))
story.append(Paragraph(
    "This project analyzes transactional retail data from the Sample Superstore dataset "
    "(9,994 order line-items, 2014\u20132017) to identify profit-draining product categories, "
    "evaluate the relationship between shipping/inventory lag and profitability, and surface "
    "actionable insights for category, regional, and discount strategy. The analysis combines "
    "SQL-based aggregation, Python (Pandas/Seaborn) exploratory analysis and correlation testing, "
    "and an interactive dashboard to communicate findings to non-technical stakeholders.",
    styles["Body"]))

# ---- Introduction ----
story.append(Paragraph("Introduction", styles["H2"]))
story.append(Paragraph(
    "Retail businesses generate large volumes of transactional data, but high sales volume does "
    "not always translate into healthy profit. The objective of this project is to move beyond "
    "top-line revenue and examine profitability at the category, sub-category, region, and "
    "discount level, in order to recommend where the business should invest, discount more "
    "cautiously, or discontinue underperforming product lines.",
    styles["Body"]))

# ---- Tools Used ----
story.append(Paragraph("Tools Used", styles["H2"]))
tools_data = [
    ["Layer", "Tool / Library", "Purpose"],
    ["Data storage & cleaning", "SQL (SQLite)", "Null/duplicate checks, profit-margin aggregation queries"],
    ["Analysis", "Python \u2013 Pandas, NumPy", "Data cleaning, feature engineering, correlation analysis"],
    ["Visualization (static)", "Matplotlib, Seaborn", "EDA charts: margin by sub-category, correlation heatmap"],
    ["Dashboard (interactive)", "Plotly (HTML)", "Filterable, browser-based dashboard for region/category/season"],
    ["Version control", "Git & GitHub", "Project hosting and documentation"],
]
t = Table(tools_data, colWidths=[3.4*cm, 4.0*cm, 9.0*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a2744")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTSIZE", (0,0), (-1,-1), 8.3),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f2f4f8")]),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)

# ---- Steps Involved ----
story.append(Paragraph("Steps Involved in Building the Project", styles["H2"]))
steps = [
    "Imported the Superstore CSV (9,994 rows, 21 columns) into SQL; validated zero null values and zero duplicate line-items.",
    "Wrote SQL queries to compute profit margin (%) by Category and Sub-Category, and to rank regions and states by profitability.",
    "Used Python/Pandas to engineer features: Profit Margin, Shipping Days (Ship Date \u2212 Order Date, used as an inventory-lag proxy), Order Month and Season.",
    "Ran Pearson correlation between Shipping Days, Discount, Sales and Profit to test whether slower fulfillment relates to lower profitability.",
    "Built Seaborn/Matplotlib charts (margin by sub-category, correlation heatmap, regional and seasonal trends, discount-vs-margin scatter).",
    "Built an interactive Plotly HTML dashboard with KPI cards and filterable region/category/time views as a portable Tableau-style deliverable.",
    "Synthesized the findings below into category, regional and discount recommendations.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(s, styles["Body"]), leftIndent=8) for s in steps],
    bulletType="bullet", start="circle", leftIndent=10
))

# ---- Key Findings ----
story.append(Paragraph("Key Findings", styles["H2"]))
findings = [
    "<b>Furniture is the profitability problem child</b>: it earns nearly as much revenue as Technology ($742K vs $836K) but only a 2.5% profit margin, versus 17.4% for Technology and 17.0% for Office Supplies.",
    "<b>Tables and Bookcases are losing money outright</b>: Tables lose $17,725 on $206,966 of sales (\u22128.6% margin); Bookcases lose $3,473 (\u22123.0% margin); Office Supplies > Supplies also loses money (\u22122.5% margin).",
    "<b>Discount is the dominant driver of lost profit, not shipping delay.</b> Discount correlates strongly negatively with profit margin (r = \u22120.86), while shipping/inventory lag shows virtually no relationship with margin (r = \u22120.01) \u2014 slow fulfillment is not what is eroding profit; aggressive discounting is.",
    "<b>The West and East regions are the most profitable</b> (14.9% and 13.5% margin respectively), while Central trails at 7.9% margin despite solid sales volume \u2014 a regional discounting or cost issue worth investigating.",
    "<b>Sales and profit do not move in lockstep</b> (r = 0.48 between Sales and Profit), confirming that revenue alone is a poor proxy for business health on this dataset.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(s, styles["Body"]), leftIndent=8) for s in findings],
    bulletType="bullet", start="circle", leftIndent=10
))

# ---- Conclusion ----
story.append(Paragraph("Conclusion", styles["H2"]))
story.append(Paragraph(
    "The analysis shows that profitability problems in this dataset are concentrated, not diffuse: "
    "two sub-categories (Tables, Bookcases) and a discounting pattern \u2014 not shipping speed \u2014 "
    "explain most of the margin erosion. Recommended actions are to (1) cap or restructure discounts "
    "on Tables, Bookcases and Supplies, where heavy discounting pushes margin negative, (2) reassess "
    "Furniture pricing and supplier costs given its 2.5% margin versus 17%+ for other categories, and "
    "(3) review Central-region pricing/discount policy to close the gap with West and East. These "
    "findings, the SQL queries, Python analysis, and interactive dashboard together form a reusable "
    "template for ongoing profitability monitoring.",
    styles["Body"]))

story.append(Spacer(1, 10))
story.append(Paragraph(
    "Dataset: Sample Superstore (Kaggle) &middot; Full code, SQL queries and dashboard: see project GitHub repository.",
    styles["Small"]))

doc = SimpleDocTemplate(
    "report/Retail_Profitability_Report.pdf",
    pagesize=A4,
    topMargin=1.6*cm, bottomMargin=1.6*cm, leftMargin=1.8*cm, rightMargin=1.8*cm
)
doc.build(story)
print("Report generated.")
