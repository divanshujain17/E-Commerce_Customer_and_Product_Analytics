# E-Commerce Analytics: Sales, Customers, Retention, and Operations

An end-to-end analytics project using the Brazilian Olist e-commerce dataset. The project combines a normalized MySQL model, reproducible Python analysis, and Power BI reporting across sales, customer value, retention, products, geography, and operations.

## Business Problem

The analysis answers a progression of business questions: how much the business sells, who buys, who returns, which customers and products are valuable, where demand is concentrated, and where operations need attention.

## Delivery Roadmap

The project is organized into four layers. `Git/` is the canonical working copy; the numbered SQL files and Python modules are the executable source of truth.

### Layer 1: Data Foundations and Customer Health

| Phase | Scope | Status | Primary deliverable |
| --- | --- | --- | --- |
| 1 | MySQL schema architecture and ingestion | Complete | Normalized DDL, keys, decimal-safe columns, and `LOAD DATA LOCAL INFILE` setup |
| 2 | Python profiling and cleansing | In progress | `python/data_quality_audit.py` for completeness, uniqueness, orphan IDs, timestamps, and IQR flags |
| 3 | Sales performance and time series | Complete | Monthly revenue, AOV, growth outputs, and executive Power BI KPIs |
| 4 | Customer segmentation and RFM scoring | Complete | Rule-based five-segment RFM output and customer visuals |
| 5 | Observed CLV and Pareto analysis | Complete | Historical customer value, ranked spend, cumulative concentration, and CLV extracts |
| 6 | Monthly cohort retention | Complete in SQL/Python | Cohort offset matrix, retention heatmap, and reusable retention extracts; Power BI matrix remains a presentation enhancement |

### Layer 2: Geographic and Logistics Fulfillment

| Phase | Scope | Status | Primary deliverable |
| --- | --- | --- | --- |
| 7 | Geographic analysis and regional penetration | Complete | State, city, ZIP, revenue density, and regional AOV queries |
| 8 | Delivery SLA and logistics bottlenecks | Complete | Delivery deltas, on-time rate, late-order analysis, and state/category breakdowns |

### Layer 3: Financial, Operational, and Experience Audits

| Phase | Scope | Status | Primary deliverable |
| --- | --- | --- | --- |
| 9 | Payments and installment analytics | Complete | Payment mix, transaction value, installments, and category payment analysis |
| 10 | Reviews and SLA impact | Data-ready, optional inputs | Review/delay queries in `sql/14_review_and_seller_extensions.sql`; review CSV is required for execution |
| 11 | Seller performance and marketplace ranking | Data-ready, optional inputs | Seller scorecard queries; seller CSV is required for execution |
| 12 | Order lifecycle and operational status | Complete | Approval, processing, carrier, delivery, cancellation, and funnel metrics |
| 13 | Catalog density and inventory dimensions | Complete | Catalog/freight analysis and unsold SKU isolation |

### Layer 4: Advanced Modeling and Predictive Intelligence

| Phase | Scope | Status | Primary deliverable |
| --- | --- | --- | --- |
| 14 | Market basket and product affinity | Complete, optional dependency | Apriori support, confidence, lift, and association-rule export |
| 15 | Demand and revenue forecasting | Added | `python/revenue_forecast.py` with seasonal exponential smoothing, holdout RMSE/MAPE, and quarterly forecast output |

### Execution order

Run `sql/01_database_setup.sql` through the numbered SQL modules in order. Run the Python modules from `Git/` with the repository root as the working directory. Generated extracts belong in `sql/reports/`; source datasets and report outputs are not mixed with analysis code.

### SQL and data setup

The numbered SQL scripts create the normalized MySQL model, load the available Olist source data, and provide analysis for each supported phase.

Run the scripts in numeric order from `sql/` after placing the CSV files in `datasets/`.

### Phase 2: Python

Open `notebook/Ecommerce_Analysis.ipynb`. It uses relative paths and writes reusable CSV outputs to `sql/reports/` for quality, RFM, CLV, cohort retention, product analysis, delivery, payment, and time series analysis.

Install the required packages with:

```text
pandas
numpy
matplotlib
seaborn
jupyter
statsmodels
mlxtend  # optional, for market basket analysis
```

### Power BI

Open `dashboard/Ecommerce_Analytics_Report.pbix` to explore the available report pages:

- Executive overview
- Customer analysis and RFM segmentation
- Product performance
- Time series performance
- Customer lifetime value and retention
- Geographic and operational analysis

The next presentation enhancement is a dedicated Customer Retention & Cohort matrix page in Power BI, followed by a forecast page using `sql/reports/revenue_forecast.csv`.

Dashboard screenshots are available in `Images/`.

## Business Questions Answered

### Executive sales answers

1. **How much revenue, how many orders, customers, and what AOV?** 
Approximately **$13.6M** in delivered-item revenue across **98.7K orders** and **93.4K unique customers**, with an overall AOV of approximately **$137.70**.
2. **Which states generate revenue?** 
**Sao Paulo** leads by a wide margin at approximately **$5.21M**, followed by Rio de Janeiro at **$1.82M** and Minas Gerais at **$1.59M**. Smaller states can show higher AOV despite lower total revenue.
3. **Which categories perform best?** 
**Beauty & Health** leads revenue at **$1.23M**, followed by Watches Gifts at **$1.17M** and Bed, Bath & Table Linens at **$1.02M**.
4. **How does revenue change over time?** 
Revenue rises through 2017, peaks in **November 2017 at approximately $987.8K**, remains strong in December and January, and then fluctuates through 2018.

### Customer and RFM answers

5. **Who are high-value and at risk?** 
The retained segmentation identifies High Value Active, High Value At Risk, Recent Low Value, At Risk, and Regular Customers. High Value Active customers have the largest segment value at approximately **$6.05M**, while High Value At Risk customers contribute approximately **$1.98M** and are the clearest re-engagement audience.
6. **How many purchase once?** 
Approximately **96.95%** of unique customers purchase once, confirming that repeat purchase and retention are the primary growth opportunity.
7. **Which segments generate revenue?** 
High Value Active contributes the most value, followed by Regular Customers at approximately **$4.02M**. High Value At Risk customers have a higher average observed value than High Value Active customers, so retention work should prioritize them despite their smaller population.

### CLV and retention answers

8. **What is observed CLV?** 
Observed CLV is historical customer revenue, not a forecast. The current report measures customer lifetime revenue, average customer value, top customers, revenue concentration, CLV by state, and CLV by category.
9. **What proportion of revenue comes from the top 10% and top 20%?** 
The notebook calculates both shares from the customer-level monetary distribution and writes the ranked data used by the Pareto chart. These are concentration measures, not predictive CLV estimates.
10. **When do customers return?** 
Cohort retention falls sharply after the first purchase month. The cohort extract and heatmap expose month 1, month 3, and month 6 retention by acquisition cohort, making the retention problem visible by timing rather than only as a one-time-buyer percentage.

### Product, geography, and operations answers

11. **Which categories attract high-value customers?** 
The CLV-by-category output ranks categories by unique customers, total revenue, and revenue per customer; category results should be interpreted alongside catalog size and order volume rather than revenue alone.
12. **Where are customers concentrated?** 
Sao Paulo dominates customers, orders, and revenue. City-level and ZIP-prefix outputs add the detail needed for ranking cities and building a bubble or filled map.
13. **How is delivery performing?** 
The operations SQL and notebook calculate average delivery days, on-time percentage, late orders, approval time, processing time, and carrier-to-customer time, with state and category breakdowns. These outputs identify operational bottlenecks without treating missing timestamps as completed deliveries.
14. **Which payment methods dominate?** 
The payment module compares payment type, payment value, average transaction value, installments, and payment method by category. Reviews, seller satisfaction, and seller-balanced scoring require the optional source files documented in `sql/14_review_and_seller_extensions.sql`.
15. **What demand should be planned for next?** 
The forecasting module validates a short-horizon revenue forecast with holdout RMSE and MAPE, then writes the next three monthly estimates to `sql/reports/revenue_forecast.csv`.

## Key Findings

- The business is large but highly retention-dependent: roughly 97% of unique customers purchase only once.
- Revenue is geographically concentrated in Sao Paulo, while several lower-volume states have higher AOVs.
- Beauty & Health, Watches Gifts, and Bed, Bath & Table Linens are the leading revenue categories in the current extract.
- November 2017 is the strongest observed revenue month.
- High Value Active customers contribute the largest observed segment revenue, while High Value At Risk customers have the highest average observed value and should be prioritized for re-engagement.
- Cohort retention declines quickly after the first purchase, which supports a dedicated retention page instead of relying on a generic customer-count visual.
- The Pareto, delivery, payment, catalog, and market-basket modules generate the detailed outputs used for dashboard decisions. Refresh the extracts before publishing final KPI captions.

## Recommendations and Suggestions

### Customer retention

- Prioritize **High Value At Risk** customers for personalized win-back campaigns because they combine high historical value with weak recent activity.
- Build a first-to-second-purchase journey for **Recent Low Value** customers using category recommendations, time-limited incentives, and post-delivery follow-up.
- Use the cohort retention matrix as the primary retention KPI. Track month 1, month 3, and month 6 retention by acquisition cohort instead of relying only on the overall repeat-customer rate.

### Commercial growth

- Protect inventory and promotional visibility for **Beauty & Health**, **Watches Gifts**, and **Bed, Bath & Table Linens**, while checking margin before increasing spend.
- Use market-basket lift results to create bundles and cross-sell recommendations; require a minimum support threshold so rare combinations do not drive unreliable campaigns.
- Compare category revenue with catalog size, price, freight, and unsold-SKU counts before expanding a category.

### Regional and operational focus

- Maintain São Paulo as the core volume market, but test regional campaigns in states with higher AOV and lower order penetration.
- Use late-order severity and on-time delivery rates to target logistics improvements by state and category rather than applying one national SLA action.
- Reconcile payment totals against order and item revenue before publishing financial KPIs, especially where installments or multiple payment rows exist.

### Data and modeling governance

- Run `python/data_quality_audit.py` before each refresh and block publication when orphan IDs, missing timestamps, or monetary outliers exceed agreed thresholds.
- Treat observed CLV and Pareto shares as historical measures, not forecasts of customer profitability.
- Refit the revenue forecast when new monthly data is available and compare it with a seasonal-naive baseline; do not use the forecast for inventory decisions until error remains stable across multiple holdout windows.
- Add the optional reviews and sellers datasets before marking Phases 10 and 11 as fully complete.

## Repository Structure

```text
Git/
├── dashboard/     Power BI report and icons
├── datasets/      Source CSV files
├── Images/        Dashboard screenshots
├── notebook/      Reproducible Python analysis
├── python/        Optional ML analysis modules
└── sql/           Database setup, phase analysis, and report extracts
```

The CSV files are retained for reproducibility. Review dataset licensing and hosting limits before publishing the repository publicly.
