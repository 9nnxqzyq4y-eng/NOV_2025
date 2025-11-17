#!/usr/bin/env bash
set -euo pipefail

# Validates input files/IDs and credentials for data ingestion.
# Produces a structured JSON output and fails with a clear error payload.
#
# Usage:
#   ./tools/validate_drive_files.sh --file-ids "file1.csv,file2.csv" --creds-json "/path/to/creds.json"
#
# Arguments:
#   --file-ids string   : Comma-separated list of local file paths or Google Drive IDs.
#                           Can also be sourced from $DRIVE_FILE_IDS.
#   --creds-json string : Path to Google Service Account JSON, the raw JSON string,
#                           or '-' to read the JSON from standard input.
#                           Can also be sourced from $GOOGLE_SERVICE_ACCOUNT_JSON.

# --- Helper Functions ---

fail() {
  local reason"$1"
  local details"$2"
  jq -n --exit-status \
    --arg reason "$reason" \
    --arg details "$details" \
    '{status: "error", reason: $reason, details: $details}' | tee "$OUTPUT_FILE" &2
  exit 2
}



# --- Main Logic ---

main() {
  # Securely create a temporary file for the output summary.
  # It will be cleaned up automatically when the script exits.
  OUTPUT_FILE$(mktemp -t ingestion_validation_summary.XXXXXX.json)
  trap 'rm -f "$OUTPUT_FILE"' EXIT

  echo "Validation summary will be written to: $OUTPUT_FILE" &2

  # Parse CLI arguments
  local FILE_IDS"${DRIVE_FILE_IDS-}"
  local CREDS_JSON"${GOOGLE_SERVICE_ACCOUNT_JSON-}"

  while [[ "$#" -gt 0 ]]; do
    case $1 in
      --file-ids)
        FILE_IDS"$2"
        shift # past argument
        ;;
      --creds-json)
        if [[ "$2"  "-" ]]; then
          # Read from stdin if argument is '-'
          CREDS_JSON$(cat)
        else
          CREDS_JSON"$2"
        fi
        shift # past argument
        ;;
      *) fail "unknown_argument" "Unknown argument provided: $1" ;;
    esac
    shift # past argument or value
  done

  # Validate required inputs
  if [ -z "$FILE_IDS" ]; then
    fail "missing_input" "DRIVE_FILE_IDS or --file-ids argument is required."
  fi
  if [ -z "$CREDS_JSON" ]; then
    fail "missing_credentials" "GOOGLE_SERVICE_ACCOUNT_JSON or --creds-json argument is required."
  fi

  # Check service account credentials
  local creds_status"invalid"
  local creds_type"none"
  if [ -f "$CREDS_JSON" ]; then
    creds_status"valid_path"
    creds_type"path"
  elif jq -e . /dev/null  "$CREDS_JSON"; then
    creds_status"valid_json_string"
    creds_type"raw_json"
  fi

  # Process file IDs
  local -a validated_files()
  local -a drive_ids()
  local -a missing_files()

  IFS',' read -r -a tokens  "$FILE_IDS"
  for token in "${tokens[@]}"; do
    local trimmed_token
    trimmed_token"${token#"${token%%[![:space:]]*}"}" # Trim leading whitespace
    trimmed_token"${trimmed_token%"${trimmed_token##*[![:space:]]}"}" # Trim trailing whitespace
    if [[ -n "$trimmed_token" && -f "$trimmed_token" ]]; then
      _validate_schemas "$trimmed_token"
      validated_files+("$trimmed_token")
    elif [[ "$trimmed_token" ! *"/"* && ${#trimmed_token} -ge 8 ]]; then
      drive_ids+("$trimmed_token")
    else
      missing_files+("$trimmed_token")
    fi
  done

  # Determine final status
  local final_status"ok"
  if [ "$creds_status"  "invalid" ] || [ ${#missing_files[@]} -gt 0 ]; then
    final_status"error"
  fi

  # Build and write JSON output
  jq -n \
    --arg status "$final_status" \
    --argjson validated_files "$(jq -n '$ARGS.positional' --args "${validated_files[@]}")" \
    --argjson drive_ids "$(jq -n '$ARGS.positional' --args "${drive_ids[@]}")" \
    --argjson missing_files "$(jq -n '$ARGS.positional' --args "${missing_files[@]}")" \
    --arg creds_status "$creds_status" \
    --arg creds_type "$creds_type" \
    '{
      status: $status,
      inputs: {
        validated_local_files: $validated_files,
        unverified_drive_ids: $drive_ids,
        missing_or_invalid_paths: $missing_files
      },
      credentials: {
        status: $creds_status,
        type: $creds_type
      }
    }' | tee "$OUTPUT_FILE"

  # Exit with appropriate status code
  if [ "$final_status"  "error" ]; then
    exit 2
  fi
  exit 0
}

main "$@"
