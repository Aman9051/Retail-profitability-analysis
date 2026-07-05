/* ===================================================================
   RETAIL BUSINESS PERFORMANCE & PROFITABILITY ANALYSIS
   SQL Queries
   Dataset: Superstore.csv  (loaded into table "orders")
   Engine tested on: SQLite (also compatible with MySQL/PostgreSQL
   with minor syntax tweaks, e.g. strftime -> DATE_FORMAT)
   =================================================================== */

/* -------------------------------------------------------------
   1. DATA CLEANING / SANITY CHECKS
   ------------------------------------------------------------- */

-- 1a. Check for missing/null values in key columns
SELECT
    SUM(CASE WHEN "Order ID"   IS NULL THEN 1 ELSE 0 END) AS null_order_id,
    SUM(CASE WHEN "Sales"      IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN "Profit"     IS NULL THEN 1 ELSE 0 END) AS null_profit,
    SUM(CASE WHEN "Category"   IS NULL THEN 1 ELSE 0 END) AS null_category,
    SUM(CASE WHEN "Region"     IS NULL THEN 1 ELSE 0 END) AS null_region
FROM orders;

-- 1b. Check for duplicate Order ID + Product ID combinations (line-item duplicates)
SELECT "Order ID", "Product ID", COUNT(*) AS cnt
FROM orders
GROUP BY "Order ID", "Product ID"
HAVING COUNT(*) > 1;

-- 1c. Row count and date range sanity check
SELECT COUNT(*) AS total_rows,
       MIN(DATE("Order Date")) AS earliest_order,
       MAX(DATE("Order Date")) AS latest_order
FROM orders;


/* -------------------------------------------------------------
   2. PROFIT MARGIN BY CATEGORY & SUB-CATEGORY
   ------------------------------------------------------------- */

-- 2a. Total sales, profit and profit margin (%) by Category
SELECT
    Category,
    ROUND(SUM(Sales), 2)                                   AS total_sales,
    ROUND(SUM(Profit), 2)                                  AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2)             AS profit_margin_pct
FROM orders
GROUP BY Category
ORDER BY profit_margin_pct DESC;

-- 2b. Total sales, profit and profit margin (%) by Sub-Category
SELECT
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2)                                   AS total_sales,
    ROUND(SUM(Profit), 2)                                  AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2)             AS profit_margin_pct,
    COUNT(*)                                                AS order_lines
FROM orders
GROUP BY Category, "Sub-Category"
ORDER BY profit_margin_pct ASC;          -- ascending = worst performers first

-- 2c. Sub-categories that are LOSING money overall (profit-draining items)
SELECT
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2)   AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit
FROM orders
GROUP BY Category, "Sub-Category"
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC;


/* -------------------------------------------------------------
   3. REGIONAL & SEASONAL PERFORMANCE
   ------------------------------------------------------------- */

-- 3a. Sales and profit by Region
SELECT
    Region,
    ROUND(SUM(Sales), 2)                       AS total_sales,
    ROUND(SUM(Profit), 2)                      AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Region
ORDER BY total_profit DESC;

-- 3b. Monthly sales trend (seasonality)
SELECT
    strftime('%Y-%m', DATE("Order Date")) AS order_month,
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- 3c. Best and worst performing States by profit
SELECT
    State,
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY State
ORDER BY total_profit ASC
LIMIT 10;                                   -- 10 worst states (flip to DESC for best)


/* -------------------------------------------------------------
   4. DISCOUNT IMPACT ON PROFITABILITY
   ------------------------------------------------------------- */

-- 4a. Average discount vs average profit margin by Sub-Category
SELECT
    "Sub-Category",
    ROUND(AVG(Discount), 3)                       AS avg_discount,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2)    AS profit_margin_pct
FROM orders
GROUP BY "Sub-Category"
ORDER BY avg_discount DESC;

-- 4b. Orders with discount > 30% and their profit outcome
SELECT
    Category, "Sub-Category", Discount, Sales, Profit
FROM orders
WHERE Discount > 0.30
ORDER BY Profit ASC
LIMIT 20;


/* -------------------------------------------------------------
   5. CUSTOMER SEGMENT PERFORMANCE
   ------------------------------------------------------------- */

SELECT
    Segment,
    ROUND(SUM(Sales), 2)                       AS total_sales,
    ROUND(SUM(Profit), 2)                      AS total_profit,
    COUNT(DISTINCT "Customer ID")              AS unique_customers
FROM orders
GROUP BY Segment
ORDER BY total_profit DESC;


/* -------------------------------------------------------------
   6. SHIPPING / INVENTORY-LAG vs PROFITABILITY
   (proxy for "inventory turnover" using Order->Ship lag in days)
   ------------------------------------------------------------- */

SELECT
    "Sub-Category",
    ROUND(AVG(JULIANDAY(DATE("Ship Date")) - JULIANDAY(DATE("Order Date"))), 2) AS avg_shipping_days,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY "Sub-Category"
ORDER BY avg_shipping_days DESC;


/* -------------------------------------------------------------
   7. TOP / BOTTOM 10 PRODUCTS BY PROFIT
   ------------------------------------------------------------- */

-- Top 10 most profitable products
SELECT "Product Name", Category, "Sub-Category",
       ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY "Product Name"
ORDER BY total_profit DESC
LIMIT 10;

-- 10 biggest loss-making products
SELECT "Product Name", Category, "Sub-Category",
       ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY "Product Name"
ORDER BY total_profit ASC
LIMIT 10;
