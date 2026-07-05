# SQL Query Results

Output of the key queries in [`queries.sql`](queries.sql), run against `data/superstore.db`. Committed here so results are viewable directly on GitHub without needing to run SQL locally.

## Profit Margin by Category

| Category        |   total_sales |   total_profit |   profit_margin_pct |
|:----------------|--------------:|---------------:|--------------------:|
| Technology      |        836154 |       145455   |               17.4  |
| Office Supplies |        719047 |       122491   |               17.04 |
| Furniture       |        742000 |        18451.3 |                2.49 |

## Profit Margin by Sub-Category (worst 6)

| Category        | Sub-Category   |   total_sales |   total_profit |   profit_margin_pct |
|:----------------|:---------------|--------------:|---------------:|--------------------:|
| Furniture       | Tables         |      206966   |      -17725.5  |               -8.56 |
| Furniture       | Bookcases      |      114880   |       -3472.56 |               -3.02 |
| Office Supplies | Supplies       |       46673.5 |       -1189.1  |               -2.55 |
| Technology      | Machines       |      189239   |        3384.76 |                1.79 |
| Furniture       | Chairs         |      328449   |       26590.2  |                8.1  |
| Office Supplies | Storage        |      223844   |       21278.8  |                9.51 |

## Sub-Categories Losing Money

| Category        | Sub-Category   |   total_sales |   total_profit |
|:----------------|:---------------|--------------:|---------------:|
| Furniture       | Tables         |      206966   |      -17725.5  |
| Furniture       | Bookcases      |      114880   |       -3472.56 |
| Office Supplies | Supplies       |       46673.5 |       -1189.1  |

## Sales & Profit by Region

| Region   |   total_sales |   total_profit |   profit_margin_pct |
|:---------|--------------:|---------------:|--------------------:|
| West     |        725458 |       108418   |               14.94 |
| East     |        678781 |        91522.8 |               13.48 |
| South    |        391722 |        46749.4 |               11.93 |
| Central  |        501240 |        39706.4 |                7.92 |

## Worst 10 States by Profit

| State          |   total_sales |   total_profit |
|:---------------|--------------:|---------------:|
| Texas          |      170188   |      -25729.4  |
| Ohio           |       78258.1 |      -16971.4  |
| Pennsylvania   |      116512   |      -15560    |
| Illinois       |       80166.1 |      -12607.9  |
| North Carolina |       55603.2 |       -7490.91 |
| Colorado       |       32108.1 |       -6527.86 |
| Tennessee      |       30661.9 |       -5341.69 |
| Arizona        |       35282   |       -3427.92 |
| Florida        |       89473.7 |       -3399.3  |
| Oregon         |       17431.2 |       -1190.47 |

## Avg Discount vs Margin by Sub-Category

| Sub-Category   |   avg_discount |   profit_margin_pct |
|:---------------|---------------:|--------------------:|
| Binders        |          0.372 |               14.86 |
| Machines       |          0.306 |                1.79 |
| Tables         |          0.261 |               -8.56 |
| Bookcases      |          0.211 |               -3.02 |
| Chairs         |          0.17  |                8.1  |
| Appliances     |          0.167 |               16.87 |
| Copiers        |          0.162 |               37.2  |
| Phones         |          0.155 |               13.49 |
| Furnishings    |          0.138 |               14.24 |
| Fasteners      |          0.082 |               31.4  |
| Envelopes      |          0.08  |               42.27 |
| Accessories    |          0.078 |               25.05 |
| Supplies       |          0.077 |               -2.55 |
| Storage        |          0.075 |                9.51 |
| Paper          |          0.075 |               43.39 |
| Art            |          0.075 |               24.07 |
| Labels         |          0.069 |               44.42 |

## Customer Segment Performance

| Segment     |     total_sales |   total_profit |   unique_customers |
|:------------|----------------:|---------------:|-------------------:|
| Consumer    |      1.1614e+06 |       134119   |                409 |
| Corporate   | 706146          |        91979.1 |                236 |
| Home Office | 429653          |        60298.7 |                148 |

## Shipping Days vs Margin by Sub-Category

| Sub-Category   | avg_shipping_days   |   profit_margin_pct |
|:---------------|:--------------------|--------------------:|
| Tables         |                     |               -8.56 |
| Supplies       |                     |               -2.55 |
| Storage        |                     |                9.51 |
| Phones         |                     |               13.49 |
| Paper          |                     |               43.39 |
| Machines       |                     |                1.79 |
| Labels         |                     |               44.42 |
| Furnishings    |                     |               14.24 |
| Fasteners      |                     |               31.4  |
| Envelopes      |                     |               42.27 |
| Copiers        |                     |               37.2  |
| Chairs         |                     |                8.1  |
| Bookcases      |                     |               -3.02 |
| Binders        |                     |               14.86 |
| Art            |                     |               24.07 |
| Appliances     |                     |               16.87 |
| Accessories    |                     |               25.05 |

## Top 10 Most Profitable Products

| Product Name                                                                | Category        | Sub-Category   |   total_profit |
|:----------------------------------------------------------------------------|:----------------|:---------------|---------------:|
| Canon imageCLASS 2200 Advanced Copier                                       | Technology      | Copiers        |       25199.9  |
| Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies | Binders        |        7753.04 |
| Hewlett Packard LaserJet 3310 Copier                                        | Technology      | Copiers        |        6983.88 |
| Canon PC1060 Personal Laser Copier                                          | Technology      | Copiers        |        4570.93 |
| HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | Technology      | Machines       |        4094.98 |
| Ativa V4110MDD Micro-Cut Shredder                                           | Technology      | Machines       |        3772.95 |
| 3D Systems Cube Printer, 2nd Generation, Magenta                            | Technology      | Machines       |        3717.97 |
| Plantronics Savi W720 Multi-Device Wireless Headset System                  | Technology      | Accessories    |        3696.28 |
| Ibico EPK-21 Electric Binding System                                        | Office Supplies | Binders        |        3345.28 |
| Zebra ZM400 Thermal Label Printer                                           | Technology      | Machines       |        3343.54 |

## 10 Biggest Loss-Making Products

| Product Name                                                      | Category        | Sub-Category   |   total_profit |
|:------------------------------------------------------------------|:----------------|:---------------|---------------:|
| Cubify CubeX 3D Printer Double Head Print                         | Technology      | Machines       |       -8879.97 |
| Lexmark MX611dhe Monochrome Laser Printer                         | Technology      | Machines       |       -4589.97 |
| Cubify CubeX 3D Printer Triple Head Print                         | Technology      | Machines       |       -3839.99 |
| Chromcraft Bull-Nose Wood Oval Conference Tables & Bases          | Furniture       | Tables         |       -2876.12 |
| Bush Advantage Collection Racetrack Conference Table              | Furniture       | Tables         |       -1934.4  |
| GBC DocuBind P400 Electric Binding System                         | Office Supplies | Binders        |       -1878.17 |
| Cisco TelePresence System EX90 Videoconferencing Unit             | Technology      | Machines       |       -1811.08 |
| Martin Yale Chadless Opener Electric Letter Opener                | Office Supplies | Supplies       |       -1299.18 |
| Balt Solid Wood Round Tables                                      | Furniture       | Tables         |       -1201.06 |
| BoxOffice By Design Rectangular and Half-Moon Meeting Room Tables | Furniture       | Tables         |       -1148.44 |

