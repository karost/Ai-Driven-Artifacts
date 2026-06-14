# Work Training — Memory & Tracking

> This file tracks project state, rules, and decisions. It lives in the repo so both me and the user can see it.

---

## CONSTITUTION — Always Follow (from SOUL.md)

1. **Explain first**: WHAT it is, HOW it works, WHY it matters — show example, then demonstrate.
2. **Never silently execute**: Declare intent (what, how, why) — then act.
3. **Never guess**: Research ≥2 sources before proposing fixes. (Post-error research.)
4. **Never install Ollama locally**: Use Ollama Cloud only.
5. **Use SearXNG/Qdrant/Firecrawl automatically**: No reminders needed.
6. **Risk research BEFORE implementation**: Produce risk register → get confirmation → THEN implement. (Pre-implementation research.)
7. **Parent gatekeeping**: Verify subagent evidence independently before accepting.

---

## PLATFORM — Target Audience

- **Hermes-Beginner-Handbook targets WINDOWS 11 users** (not Mac)
- My local Mac is only the dev machine
- All training content uses Windows 11 paths, PowerShell commands, `host.docker.internal`

### Windows 11 Directory Structure

```
C:\hermes_dev\
├── docker-linux\          ← Lab 1 Option 3: Linux container
│   ├── docker-compose.yml ← volumes: C:\hermes_dev\home:/home/thanit
│   ├── Dockerfile
│   └── .env
├── home\                  ← Volume mapped to /home/thanit inside container (Hermes config, skills, .env live here)
├── search-engine\         ← SearXNG + Firecrawl + Qdrant
│   ├── docker-compose.yml
│   ├── .env
│   ├── searxng\
│   │   └── settings.yml   ← MUST have formats: [html, json]
│   └── firecrawl-pgdata\
└── docs\training\         ← Handbook source files
```

### Key Networking

- From inside hermes-dev container → use `host.docker.internal:<port>`
- From Windows PowerShell on host → use `localhost:<port>`
- SearXNG: `host.docker.internal:8080` (container) / `localhost:8080` (host)
- Firecrawl: `host.docker.internal:3002` (container) / `localhost:3002` (host)
- Qdrant: `host.docker.internal:6333` (container) / `localhost:6333` (host)

---

## PROJECT STATUS

### Hermes-Beginner-Handbook.md — COMPLETED

- All ~99 fake CLI commands replaced with real v0.15.1 equivalents
- 5 HIGH dependency flow issues fixed
- 5 MEDIUM dependency flow issues verified/resolved
- 39 "Back to TOC" navigation links added (after Labs + before next Lab)
- No real API keys found
- Positive tone (no anxiety-inducing content)

### search-engine/search-engine.md — COMPLETED

- Rewritten for **Windows 11 target audience**
- Two Hermes options explained: Option A (Windows native, `localhost`) and Option B (Linux container, `host.docker.internal`)
- All paths use `C:\hermes_dev\`, all commands use PowerShell
- SearXNG `formats: json` marked CRITICAL (7 callouts)
- Networking table: localhost vs host.docker.internal
- Architecture diagram shows both options
- **Risk audit completed** — 13 risks found (2 CRITICAL, 2 HIGH, 4 MEDIUM, 5 LOW)
- **R1 FIXED**: All `curl` → `curl.exe` (Windows PS 5.1 compatibility)
- **R2 FIXED**: `Out-File -Encoding utf8` → `[System.IO.File]::WriteAllText()` (no BOM)
- **R3 VERIFIED**: `REDIS_URL` already correct in docker-compose.yml
- **R4 FIXED**: Ghost URL `http://127.0.0.1:2368` fixed in docker-compose.yml
- **R7 FIXED**: `.env` creation uses `WriteAllText` (no CRLF/BOM)
- **R8 FIXED**: Secret key generation simplified to `openssl rand -hex 32`

---

## DECISIONS LOG

| Date | Decision | Reason |
|------|----------|--------|
| 2026-06-12 | Replace ALL fake CLI commands with real v0.15.1 equivalents | User chose Option 1 — no disclaimers, no exercise removal |
| 2026-06-12 | Remove "What Is NOT Ready" table | Replaced with positive paragraph |
| 2026-06-12 | All "Unit" → "Lab" consistently | Terminology alignment |
| 2026-06-12 | Handbook targets Windows 11, not Mac | Lab 1 Option 3 uses `C:\hermes_dev\` paths |
| 2026-06-12 | SearXNG MUST have `formats: [html, json]` in settings.yml | Without it, 403 Forbidden on all API calls |
| 2026-06-12 | SOUL.md rules are NOT duplicated in MEMORY.md or fact_store | SOUL.md is already #1 priority in system prompt — duplication is waste |
| 2026-06-12 | search-engine.md covers two Hermes options (Windows native + Linux container) | Students may run Hermes either way — same Docker services, different addresses |

---

## REMINDERS

- Do NOT duplicate SOUL.md rules in MEMORY.md or fact_store — SOUL.md is always loaded
- Do NOT confuse local Mac dev machine with Windows 11 target audience
- Always use `C:\hermes_dev\` paths and PowerShell commands in training content
- Always use `host.docker.internal` for networking from inside Docker containers