# TAC: ai-dataset-health-zos

---

# 1) Problem & Goal
- Problem: Manual dataset audits on z/OS are slow, error-prone, and infrequent; drift in SMS policies, GDG hygiene, PDS/PDSE use, and catalog inconsistencies create risk.
- Impact: Outages, failed batch jobs, wasted DASD, and compliance gaps go unnoticed.
- Goal: Fast, safe, repeatable dataset health checks with actionable findings for storage, ops, and app teams.
- Scope: CLI-first, policy-driven rules; outputs for humans (tables) and automation (JSON), using only z/OSMF Jobs and Files APIs.
- Constraints: No Db2 dependencies; avoid other z/OS services; small, focused changes.

---

# 2) MVP Today
- Coverage: Scans HLQs/patterns or explicit lists; evaluates built-in rules with PASS/WARN/FAIL severity.
- Rules: Attribute sanity (DSORG, RECFM/LRECL/BLKSIZE), PDSE vs PDS guidance, GDG base/generation checks, SMS classes (DATA/STOR/MGMT) presence, expiration/catalog status, space/extents thresholds.
- Config: YAML policy for thresholds, allowlists, and suppressions; deterministic defaults.
- Output: Table and JSON; CI-friendly exit codes; summary counts by severity.
- Access: Uses only z/OSMF Jobs and Files APIs; no external services required.

---

# 3) Demo (CLI Output Example)
Command:
```
ai-ds-health zos scan --hlq ACME.** --rules default --format table
```

Table:
```
DATASET                 RULE                   STATUS  DETAILS
ACME.PROD.LOADLIB       PDSE_REORG_NEEDED      WARN    Member index usage 78%
ACME.TEST.SOURCE        RECFM_LRECL_MISMATCH   FAIL    RECFM=VB LRECL=137; expected FB/80
ACME.OPS.GDG.BASE       GDG_ORPHAN_GENERATION  WARN    2 uncataloged generations
ACME.SHARED.PDS         PDS_DEPRECATED         FAIL    Convert to PDSE for reliability
ACME.DATA.LARGE         SPACE_HIGH_WATERMARK   WARN    92% used, 15 extents
```

JSON (snippet):
```json
{
  "summary": {"pass": 42, "warn": 7, "fail": 3},
  "findings": [
    {
      "dataset": "ACME.TEST.SOURCE",
      "rule": "RECFM_LRECL_MISMATCH",
      "status": "FAIL",
      "details": "RECFM=VB LRECL=137; expected FB/80",
      "suggested_action": "Align RECFM/LRECL or update policy"
    }
  ]
}
```

---

# 4) Roadmap
- 0–3 months:
  - Broaden rules (VSAM LISTCAT sanity, BLKSIZE multiples, HFS/ZFS flags).
  - Parallel scanning; paging/cursoring for large catalogs.
  - Policy packs per role (storage, app, ops); better summaries.
  - CSV/JSONL output; richer exit codes for CI and gates.
- 3–6 months:
  - Baselines and suppressions with expiry; trend reports.
  - Auto-generated remediation JCL snippets; dry-run via z/OSMF Jobs.
  - GitHub/GitLab action; sample dashboards from JSON.
  - Auth hardening and profiles for z/OSMF endpoints.
- 6–12 months:
  - Rule SDK for community contributions and custom org policies.
  - Scale tests for very large HLQs; 10x performance improvements.
  - Anomaly detection on historical runs; prioritized risk scoring.
  - Signed releases, catalogs of certified rule packs.

---

# 5) Community & Ask
- What we need:
  - Early adopters with non-prod LPARs to validate scale and rules.
  - Storage/SMS and catalog SMEs to refine policies and thresholds.
  - Feedback on rule priorities and severity mappings.
- How to contribute:
  - Add rules, policies, and docs; share sample datasets/patterns.
  - Follow constraints: only z/OSMF Jobs/Files APIs; no Db2; avoid other z/OS services.
- Dev hygiene (PR checklist):
  - Keep PRs small and focused.
  - Run: `ruff .`, `black --check .`, `pytest`.
- Success metrics:
  - Datasets scanned/hour, rule coverage, false-positive rate, remediation lead time.
