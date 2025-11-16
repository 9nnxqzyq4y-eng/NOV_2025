# KPI Collection Tools - Runbook

Purpose
- Guidance to run KPI ingestion, orchestration, and optional Supabase backfill safely.

Prerequisites
- Python 3.8+ (python3)
- Required Python packages for local runs:
  - pandas, numpy
  - (optional) google-api-python-client, google-auth-httplib2, google-auth-oauthlib (for Drive access)
- Optional CLI tools:
  - gemini (automation runner)
  - SonarQube MCP CLI (analyze_file_list, toggle_automatic_analysis, mcpctl)

Files covered
- tools/collect_kpis_from_drive.py
- tools/trigger_gemini_and_sonar.sh
- tools/run_sonar_mcp.sh
- tools/supabase_backfill_ml.py

Typical local quick-run (preferred)
1. Copy `.env.example` -> `.env` and set `DRIVE_FILE_IDS` to local CSV paths.
2. Install deps:
   ```
   pip install pandas numpy
3. Run the collector:
   python3 tools/collect_kpis_from_drive.py
4. Artifacts appear in `artifacts/` (monthly_kpis.csv, revenue_breakdown_by_month.csv).

Drive-run (gated environment)
1. Ensure `GOOGLE_SERVICE_ACCOUNT_JSON` and `DRIVE_FILE_IDS` are set (via secret manager).
2. Install Google client libs:
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
3. Run collector (will fail closed if misconfigured):

Backfill to Supabase (service role required)
1. Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in environment (service role key required).
2. Prepare `PREDICTIONS_CSV` and `OUTCOMES_CSV` paths (or use artifacts).
3. Run:
   python3 tools/supabase_backfill_ml.py

SonarQube MCP workflow (operational)
- Disable automatic analysis:
  - `toggle_automatic_analysis --off` (if available)
- Run ingestion/backfill
- Analyze changed/generated files:
  - `analyze_file_list <files>` (if available)
- Re-enable automatic analysis:
  - `toggle_automatic_analysis --on` (if available)

Security notes
- Never commit secrets.
- Prefer local CSVs for development and gated service accounts in production runs.
- In CI, set CI=1 to disable external downloads.

Troubleshooting
- Collector prints JSON with `status: "metric_unavailable"` on misconfig or missing deps.
- If Google client libs missing, follow the pip install instruction above.
