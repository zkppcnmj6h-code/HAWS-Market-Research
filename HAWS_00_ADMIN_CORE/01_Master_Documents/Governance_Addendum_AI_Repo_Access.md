# Governance Addendum — AI Repository Access (Level 2: Read-Only Visibility)

**Scope:** Read-only visibility for AI assistants over designated paths.
**Principles:** Human-in-the-loop; scoped access; auditable proposals; branch protection.

## Rules
1. AI assistants may **only read** files under paths listed in `ai_access_scope.yaml`.
2. Any changes must be proposed as patches on `ai-proposals/*` branches; humans review & merge.
3. No secrets or PII may be exposed; sensitive material must be redacted or stored outside scope.
4. Coordinators maintain the scope file and signature records in `.signed/`.

## Enforcement
- `bin/haws-verify` blocks PRs if policy or signatures are missing.
- Branch protection prevents direct writes from automation.

*Owner:* Project Lead (Aaron Simpson)
*Effective:* 2025-10-09
