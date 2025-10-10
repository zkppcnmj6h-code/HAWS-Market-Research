---
document_type: release_note
workstream: HAWS_00_ADMIN_CORE
owner: Strategic Coordinator
version: v2.0.0
status: Released
created: 2025-10-09
approved_by: Strategic Advisor
---

# Release Note — v2.0.0 (Governed Read-Access Baseline)

## Summary
This release establishes the **Level-2: Governed Read-Only Visibility** baseline:
- Policy: `HAWS_00_ADMIN_CORE/01_Master_Documents/Governance_Addendum_AI_Repo_Access.md`
- Scope:  `HAWS_00_ADMIN_CORE/01_Master_Documents/ai_access_scope.yaml`
- Gate:   `VisualSystemsDesigner/HAWS_Repository_Structure/bin/haws-verify` (enforces presence of policy/scope/signatures)

## Included Communications
- `HAWS_10_PROGRAM/04_Status/Sprint2_Kickoff_Notice.md` — official launch notice for **Sprint 2: AI Read-Access**.

## Operator Notes
- Work must occur on feature branches (not `main`).
- Run `bin/haws-verify` before opening PRs.
- Tagging this baseline as `v2.0.0` anchors governance history for auditability.
