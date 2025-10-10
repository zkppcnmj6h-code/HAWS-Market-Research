---
document_type: sop
workstream: HAWS_00_ADMIN_CORE
owner: Strategic Coordinator
title: HAWS AI Access Proxy — Setup and Token Rotation
version: 1.0.0
status: Draft
created: 2025-10-09
reviewed_by: Aaron Simpson
---

# AI Access Proxy — Setup and Token Rotation (Option A → Level 2)

## Purpose
Operational procedure to create, store, use, and rotate the GitHub Personal Access Token (PAT) used by the HAWS AI Access Proxy for read-only visibility over approved paths.

## Scope
Read-only access to files enumerated in `HAWS_00_ADMIN_CORE/01_Master_Documents/ai_access_scope.yaml`. Any write or out-of-scope read is prohibited.

## Prerequisites
- GitHub account with read access to the repository.
- AWS account with access to AWS Secrets Manager (if used).
- Approved governance artifacts present:
  - `HAWS_00_ADMIN_CORE/01_Master_Documents/Governance_Addendum_AI_Repo_Access.md`
  - `HAWS_00_ADMIN_CORE/01_Master_Documents/ai_access_scope.yaml`
  - `.signed/` signatures recorded.

## Token Creation (GitHub)
1. Open GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens.
2. Repository access: Only the HAWS repository.
3. Permissions:
   - Contents: Read-only
   - Metadata: Read-only
4. Create token and copy the value once.

## Secure Storage
Option A: Local development
- Store in an environment file only on the operator machine:
  - `export HAWS_AI_READ_TOKEN="<TOKEN_VALUE>"`
- Restrict file permissions to owner read/write.

Option B: AWS Secrets Manager
- Create secret `haws/ai-read-token`.
- Put the token as the secret value.
- Grant least-privilege IAM to the proxy host or operator role to read this secret.

## Configure the Proxy
- The proxy process reads `HAWS_AI_READ_TOKEN` from environment or AWS Secrets Manager.
- The proxy enforces path filtering using `ai_access_scope.yaml`.

## Rotation Procedure
1. Generate a new token per “Token Creation”.
2. Update storage (env file or secret) with the new value.
3. Restart the proxy or reload env.
4. Revoke the old token on GitHub.
5. Record rotation in the Audit Log with timestamp, operator, and reason.

## Audit and Compliance
- All proxy requests must be logged with timestamp, requester, repo ref, and path list.
- Weekly audit: follow “Audit Log Review Process”.

## Incident Response
- Immediate token revocation if misuse suspected.
- Temporary freeze of proxy usage.
- Notify Project Lead and document the incident.

## Filing
- This SOP lives at:
  - `/HAWS_00_ADMIN_CORE/06_Governance/AI_Access_Control/ai-access-setup.md`
MDcat > "VisualSystemsDesigner/HAWS_Repository_Structure/HAWS_00_ADMIN_CORE/06_Governance/AI_Access_Control/ai-access-setup.md" <<'MD'
---
document_type: sop
workstream: HAWS_00_ADMIN_CORE
owner: Strategic Coordinator
title: HAWS AI Access Proxy — Setup and Token Rotation
version: 1.0.0
status: Draft
created: 2025-10-09
reviewed_by: Aaron Simpson
---

# AI Access Proxy — Setup and Token Rotation (Option A → Level 2)

## Purpose
Operational procedure to create, store, use, and rotate the GitHub Personal Access Token (PAT) used by the HAWS AI Access Proxy for read-only visibility over approved paths.

## Scope
Read-only access to files enumerated in `HAWS_00_ADMIN_CORE/01_Master_Documents/ai_access_scope.yaml`. Any write or out-of-scope read is prohibited.

## Prerequisites
- GitHub account with read access to the repository.
- AWS account with access to AWS Secrets Manager (if used).
- Approved governance artifacts present:
  - `HAWS_00_ADMIN_CORE/01_Master_Documents/Governance_Addendum_AI_Repo_Access.md`
  - `HAWS_00_ADMIN_CORE/01_Master_Documents/ai_access_scope.yaml`
  - `.signed/` signatures recorded.

## Token Creation (GitHub)
1. Open GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens.
2. Repository access: Only the HAWS repository.
3. Permissions:
   - Contents: Read-only
   - Metadata: Read-only
4. Create token and copy the value once.

## Secure Storage
Option A: Local development
- Store in an environment file only on the operator machine:
  - `export HAWS_AI_READ_TOKEN="<TOKEN_VALUE>"`
- Restrict file permissions to owner read/write.

Option B: AWS Secrets Manager
- Create secret `haws/ai-read-token`.
- Put the token as the secret value.
- Grant least-privilege IAM to the proxy host or operator role to read this secret.

## Configure the Proxy
- The proxy process reads `HAWS_AI_READ_TOKEN` from environment or AWS Secrets Manager.
- The proxy enforces path filtering using `ai_access_scope.yaml`.

## Rotation Procedure
1. Generate a new token per “Token Creation”.
2. Update storage (env file or secret) with the new value.
3. Restart the proxy or reload env.
4. Revoke the old token on GitHub.
5. Record rotation in the Audit Log with timestamp, operator, and reason.

## Audit and Compliance
- All proxy requests must be logged with timestamp, requester, repo ref, and path list.
- Weekly audit: follow “Audit Log Review Process”.

## Incident Response
- Immediate token revocation if misuse suspected.
- Temporary freeze of proxy usage.
- Notify Project Lead and document the incident.

## Filing
- This SOP lives at:
  - `/HAWS_00_ADMIN_CORE/06_Governance/AI_Access_Control/ai-access-setup.md`
