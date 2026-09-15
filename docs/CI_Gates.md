# CI Gates for AI-Assisted & Agent-Authored Changes

**Document:** Complementary control to POL-AI-AUP-002  
**Version:** 1.0  
**Owner:** Platform / DevSecOps + AI Governance Lead  
**Purpose:** Enforce provenance, constitution compliance, dependency hygiene, and risk-tiered review in the merge pipeline.

---

## 1. Required Labels (Provenance)

Every pull request **must** carry exactly one of:

| Label              | Meaning                                                                 |
|--------------------|-------------------------------------------------------------------------|
| `provenance:human` | Written entirely by a human with no AI assistance of substance          |
| `provenance:ai-assisted` | Human-authored with material AI drafting or completion help        |
| `provenance:agent` | Opened or substantially written by an autonomous agent                  |

False or missing labels are a policy violation and block merge.

---

## 2. AI Percentage Gate

Calculated as the proportion of changed lines attributed to AI (via commit trailers, session metadata, or approved detection tooling).

| Condition                                      | Action                                      |
|------------------------------------------------|---------------------------------------------|
| AI-attributed code ≥ 15% **and** high-severity scanner finding (SAST/SCA/secret) | **Auto-reject** until remediated            |
| AI-attributed code ≥ 40%                       | Require **second human reviewer**           |
| AI-attributed code touching auth, PII, payments, or infra | Require **traceability note** (tool, model family if known, owner sign-off) + elevated review |

---

## 3. Constitution Compliance Gate

For any change labeled `provenance:ai-assisted` or `provenance:agent`:

| Check                                                                 | Required Evidence / Enforcement                          |
|-----------------------------------------------------------------------|----------------------------------------------------------|
| Root-cause analysis present (What / How / Why)                        | Must appear in PR description or linked comment before code changes |
| Scope limited to files required by the root cause                     | Diff must not contain unrelated file deletions or renames |
| No invented variables / config values                                 | Any new variable or config key must be explicitly confirmed by human in the PR thread |
| Minimal change principle                                              | Reviewer (or automated diff-size heuristic) may reject pure drive-by refactors |
| Multi-agent safety                                                    | If multiple agents touched the same files, harness must show sequential hand-off or lock; otherwise fail |

Failure of any constitution check blocks merge until corrected or explicitly waived by AI Governance Lead (time-boxed exception).

---

## 4. Dependency & Version Pin Gate

| Rule                                                                 | Enforcement                                              |
|----------------------------------------------------------------------|----------------------------------------------------------|
| Any addition, upgrade, or removal of a runtime or build dependency   | Must be declared in PR body with package name, old version (if any), new version, and rationale |
| Lockfile changes                                                     | Must be accompanied by the declaration above             |
| Major version bumps or new direct dependencies                       | Require human confirmation comment in the PR             |
| Introduction of packages with known critical CVEs or incompatible licenses | Auto-reject                                              |

Automated check (recommended): parse `package.json` / `go.mod` / `Cargo.toml` / `requirements.txt` / etc. + lockfile diff and fail if undeclared changes exist.

---

## 5. Risk-Tiered Review SLAs (unchanged from policy, enforced in CI status)

| Tier            | Examples                              | First response     | Extra gate                                      |
|-----------------|---------------------------------------|--------------------|-------------------------------------------------|
| Low             | Docs, tests-only, tiny refactor       | 4 business hours   | 1 reviewer                                      |
| Medium          | Feature behind flag, small API        | 1 business day     | Owner + 1 reviewer                              |
| High            | Auth, payments, infra, migrations, PII| 2 business hours   | Owner + senior + security if needed; live review preferred |
| Agent-authored  | Any PR opened by an agent             | 2 business hours   | Named human owner + shepherd; agent cannot be owner |

CI must surface the tier (from labels or path rules) and block merge until the required reviewers have approved.

---

## 6. Recommended Hard Gates (Platform Implementation)

```text
# Pseudocode for CI
if provenance in ["ai-assisted", "agent"]:
    require_constitution_section_in_pr()
    require_no_undeclared_dependency_changes()
    if ai_percentage >= 0.15 and has_high_severity_findings:
        fail("AI% ≥ 15% + high-severity findings")
    if ai_percentage >= 0.40:
        require_second_reviewer()
    if touches_sensitive_paths(auth|pii|payments|infra):
        require_traceability_note()
        require_elevated_review()

if provenance == "agent":
    require_named_human_owner()
    require_shepherd_approval()
```

---

## 7. Exception Path

Temporary exceptions to any gate above must be:
- Requested in writing to AI Governance Lead
- Time-boxed (maximum 14 days unless renewed)
- Logged in the exception register
- Visible as a label on the PR (`exception:ai-gate-YYYYMMDD`)

Personal consumer accounts remain prohibited for company source or confidential data; no exception path exists for that rule.

---

## 8. Metrics to Track (quarterly)

- % of PRs with correct provenance labels
- Constitution compliance pass rate on first submission
- Undeclared dependency change rate
- Mean time to merge by provenance + tier
- Post-merge defects / vulns split by provenance
- Number of active exceptions and shadow-tool findings

---

*End of CI Gates v1.0*