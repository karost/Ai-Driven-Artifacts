# ENGINEERING · GOVERNANCE

# AI Acceptable Use Policy

**Document ID:** POL-AI-AUP-002  
**Owner:** VP Engineering / AI Governance Lead  
**Effective:** 16 September 2026  
**Review cadence:** Every 6 months, or on material tool / regulation / agent-runtime change  
**Classification:** Internal  
**Applies to:** All staff, contractors, and agents using company systems  

**Supersedes:** POL-AI-AUP-001 (2026-09-16)

Policy for the use of generative AI and AI coding agents in product, engineering, design, and internal communications. Aligns with NIST AI RMF (Govern / Map / Measure / Manage), NIST AI 600-1 (Generative AI Profile), and ISO/IEC 42001 accountability requirements.

---

## 1. Purpose

This policy lets the company use AI as a productivity coefficient without losing ownership, accountability, or trust. AI may draft. A named human ships.

It exists because unreviewed AI output in code, design, documents, and team chat produces slop, silent defects, and meat-proxy behaviour: people forwarding model output they cannot explain. That erodes collaboration faster than any single bug.

Version 002 adds explicit technical controls for agent runtimes (constitution, harness safety, CI gates) so that accountability is enforceable in the pipeline, not only in culture.

---

## 2. Scope

This policy covers all generative AI and agent tools used for company work, including but not limited to:

- Coding assistants and agents (IDE, CLI, MCP, PR bots, multi-agent systems)
- Chat models used for design, documents, tickets, incident notes, and customer-facing text
- Integrations that post AI output into Slack, email, issue trackers, or docs
- Personal or consumer accounts if used on company work (generally prohibited; see §6)
- Agent constitution files (`agents.md`, `soul.md`, or equivalent) and the harness that loads them

It does not replace security, privacy, IP, or acceptable-use policies. Where they conflict, the stricter rule wins.

---

## 3. Principles

1. A named human is the author of record for every artifact that leaves their workspace.
2. AI output informs work. It does not replace accountable judgment.
3. If you cannot explain the change in your own words, it is not assisted work. It is outsourced work and must not ship.
4. Team channels are human channels. Bots do not speak as colleagues.
5. The same quality, security, license, and review bar applies to AI-assisted work as to human-authored work. AI does not lower the bar.
6. Provenance is mandatory when it changes review path, incident response, or audit.
7. Quality culture is a control. Low-quality AI dump is not “fast.” It is unaccepted work.
8. **(New in 002)** Agents that can write code or shared artifacts must operate under a loaded constitution that enforces root-cause analysis, minimal change, no invented variables, dependency declaration, and multi-agent safety. The harness and CI pipeline must make violations visible and blocking.

---

## 4. Roles

| Role                        | Accountability                                                                 |
|-----------------------------|--------------------------------------------------------------------------------|
| **Change owner (author)**   | The person whose name is on the PR, doc, design, or message. Owns correctness, security, licensing, and the ability to explain the work. |
| **Reviewer**                | Performs a real review. Not the owner unless they paired on the work. May reject unexplained AI output or constitution violations. |
| **AI Governance Lead**      | Owns this policy, the approved-tool register, agent-constitution standards, exception process, and six-month review. |
| **Security / DevSecOps**    | Tool vendor review, MCP and data-exfil controls, CI gate implementation, incident path for AI-introduced vulns. |
| **Platform / Harness owner**| Ensures multi-agent protocols prevent result overwrites and that constitution compliance checks are enforced. |
| **Hiring manager**          | Screens for ownership, not for “never used AI.” Oral defense of take-home work is required. |
| **People manager**          | Does not tolerate repeated slop. Coaching first; performance action if the person cannot own output. |

---

## 5. Approved, Restricted, Prohibited

### 5.1 Classification

| Class         | Meaning                                                                 | Examples                                                                 |
|---------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Approved**  | May be used for listed data classes and use cases on the register.      | Company-licensed Copilot / Claude / Cursor / internal models on non-restricted repos, provided constitution is loaded for write-capable agents. |
| **Restricted**| Only for named use cases after extra controls (no-training contract, DLP, elevated review, constitution + CI gates). | Agents with repo write, production-adjacent MCP, customer-data summarization, multi-agent systems. |
| **Prohibited**| Must not be used for company work.                                      | Consumer accounts on source or confidential data; unknown MCP servers; AI posting to Slack as a person; agents that ignore or cannot load the required constitution. |

The Approved AI Tools Register is the source of truth. A tool not on the register is not approved. Request path is in §11.

### 5.2 Data that must not go into unapproved tools

- Secrets, credentials, private keys, session tokens
- Customer PII, payment data, health or other regulated data
- Unreleased product strategy, unannounced security issues
- Source from repositories marked Restricted or higher, unless the tool is approved for that class
- Anything covered by a customer contract that forbids third-party AI processors

---

## 6. Communication and Collaboration (No Meat Proxy)

This section exists because AI-to-teammate posting hides authorship and destroys the ability to tell who understands the work.

1. Do not integrate an AI assistant so that it sends messages directly to coworkers in Slack, email, or chat as if it were you.
2. You may use AI to draft a message. You send it. You own it.
3. Any AI-assisted message that proposes a design, a decision, or a code change must include a short human rationale (why this option, what was rejected, what risk remains).
4. Agents may post status to a dedicated bot channel if labeled as a bot. They may not speak in human standups, design threads, or incident command as a teammate.
5. “The model said so” is not an acceptable answer in review, incident, or planning.

---

## 7. Engineering Rules

### 7.1 Ownership

If your username is on the commit, pull request, design doc, or ticket, you own the change. Vendors are not the owner. Reviewers are not the owner unless they paired. Agents are never the owner.

### 7.2 Provenance

Every PR must declare one of: `Human-authored` / `AI-assisted` / `Agent-authored`.  
The label must change the review path when thresholds in §7.4 and the CI Gates document apply. False labeling is a policy violation.

### 7.3 Explain-or-it-does-not-ship

Before request for review, the change owner completes a self-review:

- I can explain the diff in my own words.
- I know why this design was chosen over the obvious alternatives.
- Tests cover new logic. Rollback is defined.
- Dependencies, licenses, and secrets were checked.
- I would be willing to debug this at 2 a.m.

If any box is false, do not open the PR.

### 7.4 Review path by risk

| Tier            | Examples                              | First response     | Extra gate                                      |
|-----------------|---------------------------------------|--------------------|-------------------------------------------------|
| **Low**         | Docs, tests-only, tiny refactor       | 4 business hours   | 1 reviewer                                      |
| **Medium**      | Feature behind flag, small API        | 1 business day     | Owner + 1 reviewer                              |
| **High**        | Auth, payments, infra, migrations, PII| 2 business hours   | Owner + senior + security if needed; live review preferred |
| **Agent-authored** | PR opened by an agent, any tier    | 2 business hours   | Named human owner + shepherd. Agent cannot be the owner. |

### 7.5 Same bar as human code

Peer review, automated tests, SAST/SCA, secret scan, dependency and license review apply. High-impact code, IaC, and policy logic get elevated review regardless of who typed it.

### 7.6 Agent Constitution & Harness (New in 002)

Any agent capable of writing to a repository or shared artifact **must**:

1. Load and obey the company Agent Constitution (`agents.md` / `soul.md` or equivalent approved template).
2. Perform root-cause analysis (What / How / Why) before proposing code changes.
3. Restrict edits to the minimum set of files required by the stated root cause; never delete unrelated files.
4. Never invent required variables, secrets, or configuration values; recommend only and wait for human confirmation.
5. Declare any dependency or version change with package name, old/new version, and rationale.
6. Respect multi-agent safety protocols (no concurrent writes that can overwrite results).

The platform harness and CI pipeline **must** make constitution violations visible and, where configured, blocking.  
Weaknesses in concurrent multi-agent execution (race conditions, result overwrites) are treated as control gaps and must be remediated or mitigated by sequential hand-off / locking.

Detailed constitution text and CI gate rules are maintained in companion documents:

- `agents.md` (Agent Constitution)
- `CI_Gates.md` (enforcement rules)

---

## 8. Design, Documents, and Other Non-Code Artifacts

Slop is not only code. Specs, ADRs, postmortems, and customer docs written by a model and forwarded unread are in scope.

- The named author must be able to defend every material claim, constraint, and trade-off.
- Do not paste model output into a shared doc as-is without a human pass for facts, scope, and tone.
- Citations and numbers from a model are unverified until checked.

---

## 9. Hiring, Onboarding, and Performance

AI fluency is an asset when paired with ownership. It is a liability when the person is a pass-through.

- Take-home work may use AI. The interview must include an oral defense: why this design, what you rejected, how it fails, how you tested.
- Smooth delivery with no ability to discuss the work is a no-hire signal.
- After hire, repeated inability to explain shipped AI-assisted work is a performance issue, not a tooling issue.
- Do not reward volume of AI output. Reward outcomes that the owner can defend.

---

## 10. Risk Management, Audit, and Incidents

AI use is recorded in the team risk register. Minimum rows include (non-exhaustive):

| ID example     | Risk                                              | Typical controls                                      |
|----------------|---------------------------------------------------|-------------------------------------------------------|
| AIR-COM-01     | AI posts to human channels without sign-off       | Bot-only channels, human ownership of messages        |
| AIR-ACC-01     | Author cannot explain shipped work                | Explain-or-it-does-not-ship, oral defense             |
| AIR-QUAL-01    | Compounding slop in codebase / docs               | PR size limits, AI% gates, mandatory tests            |
| AIR-SEC-01     | Vulns / license / secrets from AI code            | SAST/SCA + elevated review when AI% high              |
| AIR-AGENT-01   | Agent edits unrelated files or invents variables  | Constitution + CI compliance gates                    |
| AIR-AGENT-02   | Multi-agent result overwrite                      | Harness locking / sequential protocol                 |
| AIR-GOV-01     | Shadow AI / personal accounts                     | Tool registry, prohibition on consumer accounts       |
| AIR-OPS-01     | Missing provenance at incident time               | Commit trailers, session metadata, AI-BOM             |

Each risk has an owner, likelihood × impact score, control, status, and review date.

**Audit evidence to keep:**

- Approved tool register and versions
- PR provenance labels and review records
- CI results (including constitution and dependency gates) and exception log
- Where available: session or commit-level assistance metadata
- Loaded constitution version for agent-authored changes

Incidents involving AI-assisted or agent-authored changes are owned by the change owner. “The model generated it” or “the agent did it” is not a root cause. The missing control is.

---

## 11. New Tools and Exceptions

To add a tool, high-risk use case, or new agent runtime capability, submit to the AI Governance Lead: tool, use case, data classes, business reason, and (for write-capable agents) confirmation that the required constitution can be loaded and enforced. Triage within five business days.

- Low-risk: Governance Lead may approve.
- Restricted data or high-risk use (including multi-agent write systems): Governance committee plus privacy review if personal data is involved.

Vendor checks before approval: default training on customer data, retention/deletion, residency, SOC 2 or ISO 27001, DPA, breach notification. Tools that train on prompts by default are not approved for company source or confidential data.

Temporary exceptions are written, time-boxed, and logged. Personal consumer accounts are not an exception path for source or confidential data.

---

## 12. Violations

Examples of violations:

- Sending model output to coworkers as your own analysis
- Merging code you cannot explain
- Putting secrets or customer data into an unapproved tool
- Hiding AI authorship when the label is required
- Disabling required scanners or CI gates to land AI output
- Running a write-capable agent without the required constitution
- Allowing multi-agent overwrites that the harness cannot prevent
- Inventing required variables or silently changing dependencies

Response is proportional: coaching and revert first; access restriction; performance process; for willful data-handling breaches, security incident process.

---

## 13. Metrics

Leadership reviews these at least quarterly. Volume of AI usage is not a success metric by itself.

- Share of PRs with honest provenance labels
- Constitution compliance pass rate on first submission
- Review time and acceptance rate for AI-heavy vs human-authored changes
- Defects and vulns found after merge, split by provenance
- Undeclared dependency change rate
- Exception count and shadow-tool findings
- Incidents where the owner could not explain the change
- Multi-agent conflict / overwrite incidents

---

## 14. Related Control Set

- NIST AI RMF 1.0 and Generative AI Profile (NIST AI 600-1) — Govern, Map, Measure, Manage
- ISO/IEC 42001 — AI management system (roles, risk treatment, internal audit)
- Company information security, privacy, and IP policies
- Approved AI Tools Register (living document)
- AI risk register workbook
- **Agent Constitution (`agents.md` / `soul.md`)** — mandatory for write-capable agents
- **CI Gates document** — enforcement of AI%, constitution compliance, dependency pins, and risk-tiered review

---

## 15. Acknowledgement

By using company systems and AI tools for company work, you agree that you are the author of record for what you send, commit, and ship. AI does not hold the pager. You do.

Agents that load the company constitution accept that violations are policy breaches and must surface them to the human change owner.

---

## Document Control

| Version   | Date         | Notes                                                                 |
|-----------|--------------|-----------------------------------------------------------------------|
| 1.0       | 2026-09-16   | Initial policy: ownership, no AI-to-teammate posting, provenance, risk-tiered review, hiring defense, audit evidence. |
| **2.0**   | **2026-09-16** | **Added agent constitution requirements, harness multi-agent safety, CI gates for AI% + constitution compliance + dependency pins, expanded risk register rows, and companion documents `agents.md` + `CI_Gates.md`.** |

---

## Appendix A — Acknowledgement Form (unchanged in substance)

I have received, read, and understood POL-AI-AUP-002 (AI Acceptable Use Policy) together with the current Approved AI Tools Register and the Agent Constitution requirements.

I accept that:

- Work I send, commit, or publish remains my responsibility as author of record even when AI assisted.
- I will not allow AI to send messages to colleagues as if it were me.
- I will not place secrets, customer data, or Restricted source into unapproved tools.
- I will apply honest provenance labels and will not ship work I cannot explain.
- Write-capable agents under my control will load and obey the required constitution.
- If I do not understand any part of this policy I will ask the AI Governance Lead before using a new tool or agent capability.

**Signer information**

| Field                        | Value |
|------------------------------|-------|
| Full name                    |       |
| Role / Team                  |       |
| Company email                |       |
| Manager                      |       |
| Date of acknowledgement      |       |
| Policy version acknowledged  | 2.0 (2026-09-16) |

**Signatures**

| Employee signature | Manager signature (if required by organisation) |
|--------------------|-------------------------------------------------|

*Retain this form with HR / Governance alongside onboarding records. Failure to return the form does not release the individual from the policy; use of company systems constitutes agreement under §15.*

---

*End of POL-AI-AUP-002*