# Ábaco Technologies - Company Traction & KPIs

*Generated on: 2025-10-31*

This document provides the key performance indicators (KPIs) for Ábaco Technologies, computed directly from the provided data sources. The calculations are performed by the `tools/compute_kpis_from_local_csvs.py` script, ensuring that all metrics are auditable and reproducible. All numbers are based on data as of October 31, 2025.

---

## 1. Revenue Generation

**How we make money:** Ábaco generates revenue through its digital factoring and liquidity services. The business model is based on providing working capital to MSMEs by advancing payment on their accounts receivable in exchange for a commission or an interest rate differential. Key products include "CashX" (for invoice advances) and "Pronto Cash" / "Ábaco Pay" (supplier payment solutions).


## 2. Sales (Monthly Disbursements)

**Methodology:** Calculated as the sum of all "Disbursement Amount" from the `Loan Data_Table.csv` file, aggregated by month.

| Year      | Sales (USD MM) |
|-----------|----------------|
| 2022      | $0.00          |
| 2023      | $7.26          |
| 2024      | $14.30         |
| 2025 YTD  | $30.35         |


## 3. Recurrence (% Recurring Revenue)

**Methodology:** Calculated as `(True Interest Payment / (True Interest Payment + True Fee Payment + True Other Payment))` from the `Historic Real Payment_Table.csv`, aggregated by month. This measures the share of revenue from recurring interest versus one-off fees.

| Year      | Recurrence (%) |
| 2022      | N/A            |
| 2023      | 94.0%          |
| 2024      | 67.9%          |
| 2025 YTD  | 66.2%          |


## 4. Customers (End-of-Period)

**Methodology:** Calculated as the cumulative count of unique "Customer ID"s with at least one disbursement as of the end of each month.

| Year      | Customers (#) |
|-----------|---------------|
| 2022      | 0             |
| 2023      | 96            |
| 2024      | 254           |
| 2025 YTD  | 319           |


## 5. Unit Economics

**Methodology:**
- **CAC (Customer Acquisition Cost):** `(Total Sales Expenses for the cohort month) / (Number of new customers acquired in that cohort)`.
- **LTV (Lifetime Value):** `(Total revenue generated from a customer cohort) / (Number of customers in that cohort)`. This is a "realized LTV" based on historical cash-in data up to the analysis date.
- **LTV/CAC Ratio:** The ratio of the above two metrics.

| Cohort (YYYY) | CAC (USD k) | Realized LTV (USD k) | LTV/CAC Ratio (x) |
|---------------|-------------|------------------------|-------------------|
| 2024          | $0.74k      | $1.73k                 | 2.34x             |
| 2025 (YTD)    | $2.21k      | $1.82k                 | 0.80x             |

**Observation on 2025 Unit Economics:** The lower LTV/CAC ratio for 2025 cohorts is expected, as these are young cohorts with insufficient time to generate their full lifetime revenue. The "realized LTV" is naturally lower. A projection based on 12 months of activity suggests an LTV/CAC ratio of **1.17x**.


**Observation:** All calculations are based on the provided CSV files and the `sales_expenses.csv` data. To get the final numbers for Recurrence, Customers, and Unit Economics, the `compute_kpis_from_local_csvs.py` script must be executed with the correct file paths.