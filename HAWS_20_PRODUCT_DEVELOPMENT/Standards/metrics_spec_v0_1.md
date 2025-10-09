# Metrics Spec v0.1 — Sprint-1 (“Ingest → Score → Serve”)

## Required Event Fields (all stages)
- event_id (string, UUID)
- site_id (string)
- ts_event (ISO 8601 UTC)
- ts_ingest (ISO 8601 UTC)
- ts_scored (ISO 8601 UTC)
- ts_served (ISO 8601 UTC)

## KPIs (IDs, definitions, owners)
- feeds_integrated_pct = active_target_feeds / total_target_feeds  (Owner: Architect)
- latency_ms_event_to_api_p50 / latency_ms_event_to_api_p95 = p50/p95(served_at − event_ingested_at) ms  (Owner: Coder)
- alert_precision_proxy_sim = confirmed_correct / sampled_alerts  (Owner: Researcher)
- heat_high_minutes = minutes in high heat band per day (Δ vs. baseline)  (Owner: Coder)
- geofence_violations_ack_rate = acknowledged_violations / total_violations  (Owner: Coder)
- explain_alert_click_rate = explain_clicks / total_alerts  (Owner: Coder)
- evidence_report_generated = weekly boolean + link  (Owner: Coordinator)
- privacy_guardrail_pass = all privacy checks green (n≥5, aggregation windows, value banding)  (Owner: Architect)
- copilot_triggers_demo = count of demo triggers fired  (Owner: Coder)

## UI Telemetry
- alert_id, user_role, clicked_explain (boolean), ts_click (ISO 8601 UTC)

## Weekly Evidence Export Manifest
Path: `HAWS_20_PRODUCT_DEVELOPMENT/reports/weekly/<YYYY-WW>/manifest.json`

Schema (v0.1):
{
  "week": "YYYY-WW",
  "generated_at": "ISO-8601-UTC",
  "artifacts": [
    {"type": "csv", "path": "reports/weekly/<YYYY-WW>/evidence.csv", "sha256": "<hex>"},
    {"type": "pdf", "path": "reports/weekly/<YYYY-WW>/evidence.pdf", "sha256": "<hex>"}
  ],
  "kpi_snapshot": {
    "feeds_integrated_pct": 0,
    "latency_ms_event_to_api_p50": 0,
    "latency_ms_event_to_api_p95": 0,
    "alert_precision_proxy_sim": 0,
    "heat_high_minutes": 0,
    "geofence_violations_ack_rate": 0,
    "explain_alert_click_rate": 0,
    "evidence_report_generated": false,
    "privacy_guardrail_pass": "pass|fail",
    "copilot_triggers_demo": {"heat_forecast": 0, "new_hire_stub": 0}
  }
}

## Notes
- All timestamps UTC; all IDs stable and unique.
- Emit metrics to the shared gateway per environment once CI/CD is wired in SPEC-1A.
