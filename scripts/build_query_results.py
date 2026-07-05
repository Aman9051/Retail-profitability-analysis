"""
Runs the key SQL queries from sql/queries.sql against data/superstore.db
and writes their output as Markdown tables to sql/query_results.md.

Run:  python scripts/build_query_results.py
"""

import sqlite3
import pandas as pd

DB_PATH = "data/superstore.db"
OUT_PATH = "sql/query_results.md"

queries = {
    "Profit Margin by Category": """
        SELECT Category, ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit,
               ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS profit_margin_pct
        FROM orders GROUP BY Category ORDER BY profit_margin_pct DESC
    """,
    "Profit Margin by Sub-Category (worst 6)": """
        SELECT Category, "Sub-Category", ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit,
               ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS profit_margin_pct
        FROM orders GROUP BY Category, "Sub-Category" ORDER BY profit_margin_pct ASC LIMIT 6
    """,
    "Sub-Categories Losing Money": """
        SELECT Category, "Sub-Category", ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit
        FROM orders GROUP BY Category, "Sub-Category" HAVING SUM(Profit) < 0 ORDER BY total_profit ASC
    """,
    "Sales & Profit by Region": """
        SELECT Region, ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit,
               ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS profit_margin_pct
        FROM orders GROUP BY Region ORDER BY total_profit DESC
    """,
    "Worst 10 States by Profit": """
        SELECT State, ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit
        FROM orders GROUP BY State ORDER BY total_profit ASC LIMIT 10
    """,
    "Avg Discount vs Margin by Sub-Category": """
        SELECT "Sub-Category", ROUND(AVG(Discount),3) AS avg_discount,
               ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS profit_margin_pct
        FROM orders GROUP BY "Sub-Category" ORDER BY avg_discount DESC
    """,
    "Customer Segment Performance": """
        SELECT Segment, ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit,
               COUNT(DISTINCT "Customer ID") AS unique_customers
        FROM orders GROUP BY Segment ORDER BY total_profit DESC
    """,
    "Shipping Days vs Margin by Sub-Category": """
        SELECT "Sub-Category",
               ROUND(AVG(JULIANDAY(DATE("Ship Date")) - JULIANDAY(DATE("Order Date"))), 2) AS avg_shipping_days,
               ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS profit_margin_pct
        FROM orders GROUP BY "Sub-Category" ORDER BY avg_shipping_days DESC
    """,
    "Top 10 Most Profitable Products": """
        SELECT "Product Name", Category, "Sub-Category", ROUND(SUM(Profit),2) AS total_profit
        FROM orders GROUP BY "Product Name" ORDER BY total_profit DESC LIMIT 10
    """,
    "10 Biggest Loss-Making Products": """
        SELECT "Product Name", Category, "Sub-Category", ROUND(SUM(Profit),2) AS total_profit
        FROM orders GROUP BY "Product Name" ORDER BY total_profit ASC LIMIT 10
    """,
}


def main():
    conn = sqlite3.connect(DB_PATH)
    with open(OUT_PATH, "w") as f:
        f.write("# SQL Query Results\n\n")
        f.write(
            "Output of the key queries in [`queries.sql`](queries.sql), run against "
            "`data/superstore.db`. Committed here so results are viewable directly on "
            "GitHub without needing to run SQL locally.\n\n"
        )
        for title, q in queries.items():
            df = pd.read_sql(q, conn)
            f.write(f"## {title}\n\n")
            f.write(df.to_markdown(index=False))
            f.write("\n\n")
    conn.close()
    print(f"Wrote results for {len(queries)} queries to {OUT_PATH}")


if __name__ == "__main__":
    main()
