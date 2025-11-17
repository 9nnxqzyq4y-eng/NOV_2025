#!/usr/bin/env python3
"""
ABACO KPI Computation Tool
Computes portfolio risk KPIs like DPD and PAR from local CSV files.

import pandas as pd
import numpy as np
import argparse
import logging
from typing import Optional, Dict, Any
from datetime import datetime
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def load_csv_safely(file_path: str) -> Optional[pd.DataFrame]:
    """Load CSV file with proper error handling"""
    try:
        if not file_path:
            logger.error("File path is empty")
            return None
        df = pd.read_csv(file_path, encoding='utf-8')
        logger.info(f"Loaded {len(df)} rows from {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
def compute_portfolio_kpis(
    customer_df: pd.DataFrame,
    loan_df: pd.DataFrame,
    payment_df: pd.DataFrame,
    sales_df: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """Compute comprehensive portfolio KPIs"""
    kpis = {}
        kpis["total_customers"] = len(customer_df) if not customer_df.empty else 0
        kpis["total_loans"] = len(loan_df) if not loan_df.empty else 0
        kpis["total_payments"] = len(payment_df) if not payment_df.empty else 0
        if not loan_df.empty and "Disbursement Amount" in loan_df.columns:
            kpis["total_disbursed"] = float(loan_df["Disbursement Amount"].sum())
            kpis["avg_loan_amount"] = float(loan_df["Disbursement Amount"].mean())
        else:
            kpis["total_disbursed"] = 0.0
            kpis["avg_loan_amount"] = 0.0
        if not payment_df.empty and "True Principal Payment" in payment_df.columns:
            kpis["total_principal_collected"] = float(payment_df["True Principal Payment"].sum())
            kpis["total_principal_collected"] = 0.0
        kpis["computed_at"] = datetime.now().isoformat()
        return kpis
        logger.error(f"Error computing KPIs: {e}")
        return {"error": str(e)}
def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Compute ABACO portfolio KPIs from CSV files')
    parser.add_argument("--customer", required=True, help='Customer data CSV file')
    parser.add_argument("--loan", required=True, help='Loan data CSV file')
    parser.add_argument("--payments", required=True, help='Payment data CSV file')
    parser.add_argument("--sales-expenses", help='Sales expenses CSV file')
    parser.add_argument("--output", help='Output JSON file')
    args = parser.parse_args()
    customer_df = load_csv_safely(args.customer)
    loan_df = load_csv_safely(args.loan)
    payment_df = load_csv_safely(args.payments)
    sales_df = load_csv_safely(args.sales_expenses) if args.sales_expenses else None
    if customer_df is None or loan_df is None or payment_df is None:
        logger.error("Failed to load required data files")
        return 1
    kpis = compute_portfolio_kpis(customer_df, loan_df, payment_df, sales_df)
    if args.output:
        import json
        with open(args.output, "w") as f:
            json.dump(kpis, f, indent=2)
        logger.info(f"KPIs saved to {args.output}")
    else:
        print(json.dumps(kpis, indent=2))
    return 0
if __name__ == "__main__":
    exit(main())
