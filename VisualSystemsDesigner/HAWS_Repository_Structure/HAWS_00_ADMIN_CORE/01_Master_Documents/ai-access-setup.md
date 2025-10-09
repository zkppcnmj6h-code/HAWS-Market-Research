---
document_type: implementation_guide
title: AI Access Setup — Option A (Local Mirror + Command Mediation)
status: Adopted
version: 1.0.0
created: 2025-10-09
owner: Strategic Coordinator
reviewed_by: Strategic Advisor
requires: Governance_Addendum_AI_Repo_Access.md
applies_to: All GPT collaborators and human operators
---

# AI Access Setup — Option A (Local Mirror + Command Mediation)

**Goal:** Allow AI collaborators to **view** repository content and propose changes **without** direct credentials or write access, using a human-operated local mirror + mediated commands.

---

## 1) Principles (from Governance Addendum)

- **Read-first:** AI can **see** repo content via local mirror only.
- **Human-in-the-loop:** All write operations (commits, pushes, PRs) are performed by a human operator.
- **Traceability:** All AI-originated changes land on `ai-proposals/*` branches with a signed PR and checklist.

---

## 2) Roles

- **Operator (Strategic Coordinator)**: Runs sync and executes any accepted AI commands locally.
- **Reviewers (Project Lead + Architecture Advisor)**: Approve PRs; can request changes.
- **AI Collaborators (Custom GPTs)**: Read local files; output **copy-paste** patches/briefs/PR bodies only.

---

## 3) Minimal Tooling

- macOS or Linux shell
- `git`, `gh` (GitHub CLI), `python3` (for future automation)
- Repo cloned at: `~/Documents/Market Research/VisualSystemsDesigner/HAWS_Repository_Structure`

> If different, adjust commands below to your path.

---

## 4) Branch & Folder Conventions

- **Working branches:** `ai-proposals/<date>-<topic>` (e.g., `ai-proposals/2025-10-09-metrics-spec-edits`)
- **No direct edits on `main`**
- **All AI-originated files** must carry a header block: