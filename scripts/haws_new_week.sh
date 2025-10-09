#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <YYYY-WW>"; exit 1
fi
ROOT="HAWS_20_PRODUCT_DEVELOPMENT/reports/weekly/$1"
mkdir -p "$ROOT"
cat > "$ROOT/manifest.json" <<JSON
{
  "week": "$1",
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "artifacts": [],
  "kpi_snapshot": {
    "feeds_integrated_pct": 0,
    "latency_ms_event_to_api_p50": 0,
    "latency_ms_event_to_api_p95": 0,
    "alert_precision_proxy_sim": 0,
    "heat_high_minutes": 0,
    "geofence_violations_ack_rate": 0,
    "explain_alert_click_rate": 0,
    "evidence_report_generated": false,
    "privacy_guardrail_pass": "pass",
    "copilot_triggers_demo": {"heat_forecast": 0, "new_hire_stub": 0}
  }
}
JSON
touch "$ROOT/.gitkeep"
echo "Created $ROOT with starter manifest.json"
