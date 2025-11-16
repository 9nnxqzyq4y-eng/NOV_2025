# Ábaco Technologies — Company Profile (English)

Company summary

- Who: Ábaco provides agile, transparent, 100% digital working-capital financing to micro, small and medium enterprises (MIPYMEs), guaranteeing short-term liquidity.
- Impact: Enables MIPYMEs to operate without interruptions, scale and create jobs.
- Start of operations: July 2023
- Operating markets: El Salvador, Guatemala, Costa Rica

Headlines and primary KPIs

- Primary KPIs: Revenue, NPLs (PAR30, PAR60, PAR90), Churn, APR, NIMAL (Net Interest Margin After Loss)
- Expected monthly KPIs (computed by the repo tooling):

  - Sales (monthly disbursements; USD)
  - Revenue (monthly cash-in: interest + fees + other; USD)
  - Recurrence (% recurring revenue = interest / (interest + fees + other))
  - Customers EOP (cumulative unique customers with at least one disbursement as of month end)
  - Unit economics (per cohort / month): CAC (USD k), Realized LTV (USD k), LTV/CAC (x)

Team (high level)

- Alejandro McCormack — CEO (ex-Product @ N26; Mgmt @ Raisin)
- Juan Carlos Gómez — CTO (ex-Unicomer)
- Moisés Hasbún — COO (ex-CEO C-Presta)
- Jeninefer Deras — Head of Commercial
- Carlos Villalobos — CCO
- Bárbara Mena — Head of Data & Risk

Cap table / investors (high level)

- Founders / major holders: Alejandro McCormack (~26.83%), Moisés Hasbún (~22.62%), Carlos Villalobos (~26.83%)
- Notable investors: Caricaco, Nazca, Innogen
- Last round: Pre-seed — amount raised: $1M; post-money valuation reported ~$7.5M

Product / Business model

- Product: Working capital financing secured against customers' accounts receivable.
- Revenue generation: interest on outstanding balances + periodic fees + other service charges.
- Recurrence: measure share of interest (recurring) versus one-off fees.
- Distribution / GTM: B2B sales and partnerships (e.g., ProntoCash, corporate distribution channels).
- Unique selling proposition: Competitive rates and a fully digital, fast disbursement process (typically <24 hours).

Market sizing and traction

- TAM: USD $31.28B
- SAM: USD $18.33B
- SOM: USD $180–460M
- Break-even: January 2024 (internal target)
- Target customers: MIPYMEs needing immediate liquidity
- Geographic focus: Central America and Andean region

Unit economics & financials

- CAC, LTV, and LTV/CAC must be computed from the canonical monthly artifacts produced by the ingestion pipeline.
- Use the repo tooling to generate cohort-level realized LTV and CAC from:
  - Disbursement data (loan tape)
  - Historic payments (cash-in)
  - Commercial expenses (sales expense per month)
- Note: LTV in this project is "realized LTV" computed from observed cash-in up to the analysis date (conservative, lower-bound).

Data & governance requirements

- All KPIs must be sourced from validated artifacts (artifacts/monthly_kpis.csv and artifacts/unit_economics.csv).
- Any change to canonical formulas (LTV, CAC, DPD buckets, PD thresholds, SFV index) is a breaking change and requires:
  - Documentation of rationale
  - Unit tests and reconciliation examples
  - ABACO_CFO_AI sign-off

Run instructions (compute real numbers locally)

```bash
python3 tools/compute_kpis_from_local_csvs.py \
  --customer "./data/Abaco - Loan Tape_Customer Data_Table.csv" \
  --loan "./data/Abaco - Loan Tape_Loan Data_Table.csv" \
  --payments "./data/Abaco - Loan Tape_Historic Real Payment_Table.csv" \
  --schedule "./data/Abaco - Loan Tape_Payment Schedule_Table.csv" \
  --collateral "./data/Abaco - Loan Tape_Collateral_Table.csv" \
  --sales-expenses "./data/sales_expenses.csv" \
  --output-dir "./artifacts"
```

Outputs produced:

- artifacts/monthly_kpis.csv — month, sales_usd_mm, revenue_usd_mm, recurrence_pct, customers_eop
- artifacts/unit_economics.csv — cohort, sales_expense_usd, new_customers, CAC_usd_k, realized_LTV_usd_k, LTV_over_CAC_x
- artifacts/summary.json — summary and file paths

Audit & handoff

- Keep artifacts and validation.json (if produced) in secured storage and include SHA256 + timestamp in PR description.
- Request reviewers: @coderabbit (data & operational), @sourcery (code quality), ABACO_CFO_AI (financial governance sign-off).

Contact & references

- For operational runbook and SonarQube MCP instructions see:
  - .github/instructions/sonarqube_mcp.instructions.md
  - tools/README_COLLECT_KPIS.md

<!-- End of profile -->

