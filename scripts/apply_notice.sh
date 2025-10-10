# File: scripts/apply_notice.sh
#!/usr/bin/env bash
# Minimal, idempotent writer for the finalized Sprint-1 notice.
set -euo pipefail

ROOT_DEFAULT="/Users/aaronsimpson/Documents/Market Research"
ROOT="${1:-$ROOT_DEFAULT}"
TARGET="$ROOT/HAWS_10_PROGRAM/04_Status/Sprint1_Repository_Deployment_Notice.md"
REPO_URL="https://github.com/zkppcnmj6h-code/HAWS-Market-Research.git"

mkdir -p "$(dirname "$TARGET")"

if [ -f "$TARGET" ]; then
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  cp "$TARGET" "${TARGET}.bak.${ts}"
  echo "Backed up: ${TARGET}.bak.${ts}"
fi

# --- Write the clean, fenced, GitHub-ready Markdown ---
cat > "$TARGET" <<'MD'
# Sprint-1 Repository Deployment Notice  
**Ingest → Score → Serve**

**From:** Architecture Advisor  
**To:** Project Lead, Strategic Coordinator, Architect, Coder, Researcher, Market Research Lead  
**Date:** 2025-10-09  

---

## 1. Summary

The Architecture Advisor confirms that the **HAWS-Market-Research** repository has been successfully initialized, structured, and deployed on GitHub.

🔗 **Repository:** https://github.com/zkppcnmj6h-code/HAWS-Market-Research

This deployment establishes the **canonical source of truth** for all HAWS Sprint-1 deliverables and transitions the initiative from planning to execution.

---

## 2. Deployment Highlights

| Component | Status | Details |
|---|---|---|
| **Repository Structure** | ✅ Complete | HAWS domain hierarchy implemented (`HAWS_10_PROGRAM`, `HAWS_20_PRODUCT_DEVELOPMENT`, etc.) |
| **Core Files** | ✅ Added | `Sprint1_Execution_Addendum.md`, `metrics_spec_v0_1.md`, `Sprint1_Week1_Summary.md`, `haws_new_week.sh` |
| **Version Control** | ✅ Established | Local Git initialized and synced to remote; `.gitignore` configured for macOS/Office temp files |
| **Authentication** | ✅ Secured | GitHub CLI authenticated as `zkppcnmj6h-code` (HTTPS protocol) |
| **Remote Tracking** | ✅ Linked | `main` branch tracking `origin/main` (live on GitHub) |

---

## 3. Role-Specific Instructions

### Project Lead
- Tag the baseline release:
```bash
git tag -a v1.0.0 -m "Sprint-1 Baseline (Ingest → Score → Serve)"
git push origin v1.0.0