Sprint-1 Execution Addendum — “Ingest → Score → Serve”

From: Market Research Lead
To: Architect, Coder, Researcher, Coordinator
Use With: Leadership Principles Manifesto + Role Briefs

1) Decision-Grade KPI Instrumentation (spec v0.1)

Purpose: Guarantee that engineering outputs map to business evidence the Strategic Advisor will use to assess sprint success.

Metric (ID)	Definition (formula)	Event source(s)	Sampling & rollup	Owner
feeds_integrated_pct	(# active target feeds integrated) / (total target feeds)	Ingest hub registry	Daily; %	Architect
latency_ms_event_to_api_p50/p95	Median/95th percentile of (served_at – event_ingested_at) in ms	Ingest (ts_ingest), Score (ts_scored), Serve (ts_served)	Rolling 24h; histogram	Coder
alert_precision_proxy_sim	% of sampled alerts confirmed correct in simulation review	Simulation log + reviewer labels	2×/week; %	Researcher
heat_high_minutes	Minutes per day site/team spent in “high heat band”	Score engine (WBGT/HI band)	Daily; minutes (+/– vs. baseline)	Coder
geofence_violations_ack_rate	acknowledged_violations / total_violations	Serve alert stream	Daily; %	Coder
explain_alert_click_rate	explain_clicks / total_alerts	UI telemetry	Daily; %	Coder
evidence_report_generated	Boolean + link to weekly export (PDF/CSV)	Serve export job	Weekly; Y/N + path	Coordinator
privacy_guardrail_pass	n≥5, time aggregation, value banding checks all green	Serve/privacy middleware	Weekly; pass/fail + notes	Architect
copilot_triggers_demo	Count of demo triggers fired (heat_forecast, new_hire_stub)	Event bus	Weekly; counts	Coder

Implementation notes (exact fields):
• All pipeline stages must attach: event_id, site_id, ts_event, ts_ingest, ts_scored, ts_served.
• UI telemetry: log alert_id, user_role, clicked_explain:boolean, ts_click.
• Evidence export: persist weekly artifact path and SHA in a manifest: reports/weekly/<YYYY-WW>/manifest.json.

2) Coordinator Weekly Summary — Ready-to-Use Template (Week 1)

Purpose: Provide consistent, investor-ready reporting that reflects the validated synthesis.

Headline (one line):
“From siloed signals to preventive action — HAWS served decision-grade safety intelligence in real time.”

1) KPI Snapshot (rollup for Week 1):
• Feeds integrated: {x}/{y} ({feeds_integrated_pct}%)
• Latency p50/p95: {p50} ms / {p95} ms
• Alert precision (sim): {precision}% (n={sampled})
• Heat high-band minutes: {mins} (Δ vs. baseline {delta})
• Geofence ack rate: {ack_rate}%
• Explain-alert CTR: {ctr}%
• Evidence report: {Y/N} (link)
• Privacy guardrails: {pass/fail} (notes)
• Copilot triggers (demo): heat_forecast={n1}, new_hire_stub={n2}

2) Highlights (≤3 bullets):
• {impact statement tied to KPI}
• {engineering milestone completed}
• {partner/user validation note}

3) Blockers & Decisions Needed (≤3):
• {blocker + owner + due date}

4) Changes vs. Plan (scope/time/risk):
• {delta with rationale and mitigation}

5) Next 7 Days — Commitments (per DRI):
• Architect — {commitment}
• Coder — {commitment}
• Researcher — {commitment}
• Coordinator — {commitment}

Footer: Links to weekly evidence report + logs.

3) Messaging Angles (pre-validated; paste into comms)
• Value: “Predictive, privacy-first safety intelligence that turns fragmented site data into action before incidents.”
• Proof: “Leading indicators + insurer-style evidence reports; demo shows closed loop: See Risk → Act → Document.”
• Trust: “Team-level views (n≥5), time aggregation, value banding; no biometrics, no emotion recognition.”
• Why now: “Cost pressure, insurer incentives, and mature APIs make proactive safety both possible and necessary.”

4) Role-Specific Micro-Briefs (Sprint-1 scope only)

Architect (system integrity):
• Define the ingest registry and target feed list; expose /metrics/feeds endpoint.
• Enforce privacy guardrails in Serve layer (n≥5, aggregation windows, banding).
• Deliver manifest structure for weekly evidence exports.

Coder (pipeline & UI):
• Wire timestamps at each stage; emit latency metrics.
• Implement explain_alert telemetry and geofence ack flow.
• Produce weekly export job (CSV + PDF stub) and write manifest.

Researcher (validation & proof):
• Run 2 simulation review sessions; label alert precision sample.
• Draft the Week-1 evidence narrative (3 bullets) matching KPI changes.
• Maintain a citation log for any claims used in Coordinator’s summary.

Coordinator (rhythm & hygiene):
• Publish Monday task map; Wednesday blocker list; Friday change log.
• Assemble Week-1 Summary using the template; attach evidence artifact and manifest.

5) Filing & Naming (for immediate use)
• Metrics spec: /HAWS_20_PRODUCT_DEVELOPMENT/Standards/metrics_spec_v0_1.md
• Weekly manifest root: /HAWS_20_PRODUCT_DEVELOPMENT/reports/weekly/
• Coordinator summaries: /HAWS_10_PROGRAM/04_Status/Sprint1_Week1_Summary.md
