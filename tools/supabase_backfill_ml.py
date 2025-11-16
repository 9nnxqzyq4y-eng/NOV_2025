#!/usr/bin/env python3
"""
tools/supabase_backfill_ml.py

Backfill ml.model_versions, ml.loan_predictions, ml.outcome_feedback from CSV artifacts.

Environment:
 - SUPABASE_URL (e.g., https://<project>.supabase.co)
 - SUPABASE_SERVICE_ROLE_KEY (service-role key)
 - PREDICTIONS_CSV: path (optional)
 - OUTCOMES_CSV: path (optional)


Behavior:
 - Validates env and files.
 - POSTs rows via Supabase REST (requires service role key).
 - Prints a JSON summary of inserted counts.
from __future__ import annotations
import os
import sys
import json
from typing import List, Dict
def fail_closed(reason: str, details: dict | None: Optional[str] = None) -> None:
    payload = {"status": "failed", "reason": reason}
    if details:
        payload["details"] = details
    print(json.dumps(payload))
    sys.exit(2)

try:
    import pandas as pd  # type: ignore
    import requests  # type: ignore
except (ValueError, TypeError, KeyError) as e:
    fail_closed("missing_python_deps", {"pip": "pip install pandas requests"})

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
if not SUPABASE_URL or not SUPABASE_KEY:
    fail_closed("missing_supabase_credentials", {"envs": ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"]})

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_model_version_id(model_name: str, version_number: int) -> str | None:
    """Fetch the UUID of an existing model version."""
    url = f"{SUPABASE_URL}/rest/v1/ml.model_versions?model_name=eq.{model_name}&version_number=eq.{version_number}&select=id"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200 and resp.json():
        return resp.json()[0].get("id")
    return None

def post_rows(table: str, rows: List[Dict]) -> int:
    if not rows:
        return 0
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    resp = requests.post(url, headers=HEADERS, json=rows)
    if resp.status_code not in (200, 201):
        fail_closed("supabase_insert_failed", {"table": table, "status": resp.status_code, "body": resp.text})
    # Return count inserted
    return len(resp.json())

def main() -> None:
    predictions_csv = os.environ.get("PREDICTIONS_CSV", "artifacts/predictions_to_seed.csv")
    outcomes_csv = os.environ.get("OUTCOMES_CSV", "artifacts/outcomes_to_seed.csv")

    inserted_counts = {"model_versions": 0, "loan_predictions": 0, "outcome_feedback": 0}
    model_version_id: Optional[str] = None

    # Step 1: Ensure a baseline model version exists and get its ID.
    model_version = {
        "model_name": "PD_MODEL",
        "version_number": 1,
        "description": "Initial backfill",
        "is_active": True
    }
    
    model_version_id = get_model_version_id(model_version["model_name"], model_version["version_number"])

    if model_version_id:
        print(json.dumps({"status": "info", "note": "Model version already exists, skipping creation.", "model_version_id": model_version_id}))
    else:
        print(json.dumps({"status": "info", "note": "Creating initial model version..."}))
        try:
            inserted_mv_count = post_rows("ml.model_versions", [model_version])
            inserted_counts["model_versions"] = inserted_mv_count
            model_version_id = get_model_version_id(model_version["model_name"], model_version["version_number"])
            print(json.dumps({"status": "info", "note": "Model version created.", "model_version_id": model_version_id}))
        except Exception as e:
            fail_closed("model_version_creation_failed", {"error": str(e)})

    # Step 2: Backfill predictions, linking them to the model version.
    if os.path.exists(predictions_csv):
        dfp = pd.read_csv(predictions_csv, dtype=str)
        rows = []
        for _, r in dfp.iterrows():
            rows.append({
                "loan_id": str(r.get("loan_id", "")),
                "customer_id": str(r.get("customer_id", "")),
                "model_version_id": model_version_id,
                "prediction_timestamp": r.get("prediction_timestamp"),
                "predicted_probability_of_default": float(r.get("predicted_probability_of_default") or 0) if r.get("predicted_probability_of_default") else None,
                "predicted_ltv_usd": float(r.get("predicted_ltv_usd") or 0) if r.get("predicted_ltv_usd") else None,
                "features_used": json.loads(r.get("features_used")) if r.get("features_used") else None
            })
        if rows:
            inserted_counts["loan_predictions"] = post_rows("ml.loan_predictions", rows)
        print(json.dumps({"status": "info", "note": f"Predictions CSV not found at {predictions_csv}, skipping."}))

    # Step 3: Backfill outcomes.
    if os.path.exists(outcomes_csv):
        dfo = pd.read_csv(outcomes_csv, dtype=str)
        rows = []
        for _, r in dfo.iterrows():
            rows.append({
                "prediction_id": int(r.get("prediction_id")) if r.get("prediction_id") else None,
                "actual_loan_status": r.get("actual_loan_status") or None,
                "actual_payback_date": r.get("actual_payback_date") or None,
                "actual_total_repayment_usd": float(r.get("actual_total_repayment_usd")) if r.get("actual_total_repayment_usd") else None,
                "user_feedback_rating": int(r.get("user_feedback_rating")) if r.get("user_feedback_rating") else None,
                "user_comments": r.get("user_comments") or None
            })
        if rows:
            inserted_counts["outcome_feedback"] = post_rows("ml.outcome_feedback", rows)
    else:
        print(json.dumps({"status": "info", "note": f"Outcomes CSV not found at {outcomes_csv}, skipping."}))

    print(json.dumps({"status": "ok", "inserted_counts": inserted_counts}))

if __name__ == "__main__":
    main()
