#!/usr/bin/env bash
set -euo pipefail

# ABACO End-to-End Orchestrator
# This script provides a safe, end-to-end runner for the ABACO data and analysis pipeline.
#
# Execution Flow:
# 1. Loads environment variables from .env if it exists.
# 2. Disables SonarQube automatic analysis (if MCP tools are present).
# 3. Triggers the primary ingestion and analysis orchestrator.
# 4. Runs SonarQube analysis on changed/specified files.
# 5. Optionally runs a Supabase backfill script if credentials are configured.
# 6. Re-enables SonarQube automatic analysis.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "========================================"
echo "  ABACO End-to-End Runner"
echo "========================================"
echo "Repository Root: $REPO_ROOT"
echo "Timestamp: $(date -u -Iseconds)"
echo "----------------------------------------"

# --- Helper Functions ---
find_command() {
  for cmd in "$@"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      echo "$cmd"
      return 0
    fi
  done
  return 1
}

# --- Initial Setup & Validation ---
echo "[SETUP] Validating environment..."

# Safely load .env file if it exists
if [ -f ".env" ]; then
  echo "  - Loading environment variables from .env file..."
  while IFS= read -r line || [[ -n "$line" ]]; do
    # Ignore comments and empty lines
    if [[ ! "$line" =~ ^\s*# && "$line" =~ = ]]; then
      export "$line"
    fi
  done < .env
else
  echo "  - No .env file found, skipping."
fi

PYTHON_CMD="$(find_command python3 python)"
if [ -z "$PYTHON_CMD" ]; then
  echo "  - ❌ ERROR: No Python interpreter (python3 or python) found in PATH. Aborting."
  exit 1
else
  echo "  - ✅ Python interpreter found: $PYTHON_CMD"
fi

# --- Script Definitions ---
TRIGGER_SCRIPT="tools/trigger_gemini_and_sonar.sh"
BACKFILL_SCRIPT="tools/supabase_backfill_ml.py"
TOGGLE_CMD="$(find_command toggle_automatic_analysis mcpctl)"
ANALYZE_CMD="$(find_command analyze_file_list mcpctl)"

echo "----------------------------------------"
echo "[ORCHESTRATION] Starting main pipeline..."

# Step 1: Disable automatic analysis (if available)
if [ -n "$TOGGLE_CMD" ]; then
  echo "  - Disabling automatic analysis via: $TOGGLE_CMD"
  if [ "$TOGGLE_CMD" = "mcpctl" ]; then
    mcpctl toggle-analysis --off || echo "  - Warning: mcpctl toggle-analysis failed."
  else
    "$TOGGLE_CMD" --off || echo "  - Warning: toggle_automatic_analysis failed."
  fi
else
  echo "  - SonarQube MCP toggle command not found. Skipping disable step."
fi

# Step 2: Trigger primary ingestion and analysis script
if command -v gemini >/dev/null 2>&1; then
  echo "  - Attempting ingestion via 'gemini run collect_kpis'..."
  if gemini run collect_kpis; then
    echo "  - Gemini task succeeded."
  else
    echo "  - Warning: Gemini task failed. Falling back to local collector."
    "$PYTHON_CMD" tools/compute_kpis_from_local_csvs.py --customer data/Abaco\ -\ Loan\ Tape_Customer\ Data_Table.csv --loan data/Abaco\ -\ Loan\ Tape_Loan\ Data_Table.csv --payments data/Abaco\ -\ Loan\ Tape_Historic\ Real\ Payment_Table.csv --sales-expenses data/sales_expenses.csv
  fi
else
  echo "  - Gemini CLI not found. Attempting local collector directly."
  if [ -f "tools/compute_kpis_from_local_csvs.py" ]; then
    echo "  - Running local collector: $PYTHON_CMD tools/compute_kpis_from_local_csvs.py"
    "$PYTHON_CMD" tools/compute_kpis_from_local_csvs.py --customer data/Abaco\ -\ Loan\ Tape_Customer\ Data_Table.csv --loan data/Abaco\ -\ Loan\ Tape_Loan\ Data_Table.csv --payments data/Abaco\ -\ Loan\ Tape_Historic\ Real\ Payment_Table.csv --sales-expenses data/sales_expenses.csv
  else
    echo "  - Error: No collector script found. Aborting ingestion."
    exit 1
  fi
fi

# Step 3: Build file list and run SonarQube analysis
FILES_TO_ANALYZE_EXPANDED=()
if [ -n "${FILES_TO_ANALYZE-}" ]; then
  IFS=',' read -r -a tmp <<< "$FILES_TO_ANALYZE"
  for f in "${tmp[@]}"; do
    f_trim=$(echo "$f" | xargs) # More portable trim
    [ -n "$f_trim" ] && FILES_TO_ANALYZE_EXPANDED+=("$f_trim")
  done
fi

if [ "${#FILES_TO_ANALYZE_EXPANDED[@]}" -eq 0 ]; then
  echo "  - FILES_TO_ANALYZE not set. Using git to find changed files as a fallback."
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    while IFS= read -r f; do [ -n "$f" ] && FILES_TO_ANALYZE_EXPANDED+=("$f"); done < <(git status --porcelain | awk '{print $2}')
  fi
fi

if [ "${#FILES_TO_ANALYZE_EXPANDED[@]}" -gt 0 ] && [ -n "$ANALYZE_CMD" ]; then
  echo "  - Analyzing files via: $ANALYZE_CMD"
  echo "    Files to analyze:"
  for f in "${FILES_TO_ANALYZE_EXPANDED[@]}"; do echo " - $f"; done
  if [ "$ANALYZE_CMD" = "mcpctl" ]; then
    mcpctl analyze-files "${FILES_TO_ANALYZE_EXPANDED[@]}" || echo "  - Warning: mcpctl analyze-files returned non-zero."
  else
    "$ANALYZE_CMD" "${FILES_TO_ANALYZE_EXPANDED[@]}" || echo "  - Warning: analyze_file_list command returned non-zero."
  fi
else
  echo "  - SonarQube MCP analyze command not found or no files to analyze. Skipping analysis."
fi

echo "----------------------------------------"
echo "[BACKFILL] Checking for Supabase backfill task..."

# Step 4: Optional backfill to Supabase
if [ -n "${SUPABASE_URL-}" ] && [ -n "${SUPABASE_SERVICE_ROLE_KEY-}" ]; then
  if [ -f "$BACKFILL_SCRIPT" ]; then
    echo "  - Supabase credentials detected. Running backfill: $BACKFILL_SCRIPT"
    "$PYTHON_CMD" "$BACKFILL_SCRIPT"
  else
    echo "  - Warning: Backfill script not found at $BACKFILL_SCRIPT. Skipping."
  fi
else
  echo "  - SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not set. Skipping Supabase backfill."
fi

echo "----------------------------------------"
echo "[CLEANUP] Finalizing run..."

# Step 5: Re-enable automatic analysis
if [ -n "$TOGGLE_CMD" ]; then
  echo "  - Re-enabling automatic analysis via: $TOGGLE_CMD"
  if [ "$TOGGLE_CMD" = "mcpctl" ]; then
    mcpctl toggle-analysis --on || echo "  - Warning: mcpctl toggle-analysis failed."
  else
    "$TOGGLE_CMD" --on || echo "  - Warning: toggle_automatic_analysis failed."
  fi
else
  echo "  - SonarQube MCP toggle command not found. Skipping re-enable step."
fi

echo "========================================"
echo "  ABACO Run Complete"
echo "========================================"
