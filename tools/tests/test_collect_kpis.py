import os
import subprocess
import json


def test_collect_kpis_fails_closed_if_no_env(monkeypatch):
    # Ensure required envs are not present
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_JSON", raisingFalse)
    monkeypatch.delenv("DRIVE_FILE_IDS", raisingFalse)

    proc  subprocess.run(
        ["python3", "tools/collect_kpis_from_drive.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    # Collector must exit non-zero and print JSON with status 'metric_unavailable'
    assert proc.returncode ! 0
    try:
        payload  json.loads(proc.stdout.strip())
    except Exception:
        payload  {}
    assert payload.get("status")  "metric_unavailable"
