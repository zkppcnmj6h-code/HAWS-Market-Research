---
document_type: procedure
workstream: HAWS_00_ADMIN_CORE
owner: Strategic Coordinator
title: Weekly Audit — AI Access Proxy Logs
version: 1.0.0
status: Draft
created: 2025-10-09
reviewed_by: Aaron Simpson
---

# Weekly Audit — AI Access Proxy Logs

## Purpose
Ensure AI read-access remains compliant with governance, scope, and least-privilege principles.

## Inputs
- Proxy audit log for the week.
- `ai_access_scope.yaml` (source of truth for allowed paths).
- Signatures in `.signed/`.

## Checklist
1. Retrieve weekly audit logs.
2. Verify each entry:
   - Request timestamp present
   - Requester identity present
   - Repo ref (branch/commit) present
   - Requested paths present
3. Validate scope:
   - All requested paths are within `allowed_paths` in `ai_access_scope.yaml`.
4. Anomaly scan:
   - High volume or repeated access to same file?
   - Access to unusually sensitive folders?
   - Access outside normal hours?
5. Findings:
   - List non-compliant entries or “None”.
   - Recommended actions: revoke token, rotate, narrow scope, notify lead.
6. Sign-off:
   - Auditor name, date, “Approved” or “Action Required”.

## Escalation
- Any out-of-scope read triggers immediate notification to Project Lead.
- Token rotation and proxy freeze if required.

## Filing
- Store weekly reports under:
  - `/HAWS_00_ADMIN_CORE/06_Governance/AI_Access_Control/Audit_Reports/YYYY/WW-audit.md`
