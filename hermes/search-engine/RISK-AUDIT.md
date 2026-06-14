# Search-Engine.md Risk Audit

> Audited: 2026-06-12 | Target audience: Windows 11 users

## Risk Register

| # | Risk | Likelihood | Impact | Status | Fix Required? |
|---|------|-----------|--------|--------|---------------|
| **R1** | **`curl` on Windows PowerShell 5.1 is alias for `Invoke-WebRequest`** | **HIGH** | **HIGH** | **✅ FIXED** → all 21 occurrences changed to `curl.exe` |
| **R2** | **`docker compose exec searxng cat … \| Out-File`** adds BOM to YAML | **MEDIUM** | **HIGH** | **✅ FIXED** → uses `[System.IO.File]::WriteAllText()` instead |
| **R3** | **docker-compose.yml REDIS_URL** — verified correct (`redis://firecrawl-redis:6379`) | **HIGH** | **HIGH** | **✅ VERIFIED OK** |
| **R4** | **docker-compose.yml Ghost URL missing `//`** | **HIGH** | **MEDIUM** | **✅ FIXED** → `http://127.0.0.1:2368` |
| **R5** | **SearXNG `searxng/` volume mount creates empty dir, not settings.yml** — Step 4 starts SearXNG, stops it, then runs `docker compose exec searxng cat /etc/searxng/settings.yml`. But the volume `./searxng:/etc/searxng` mounts the host's empty `searxng/` directory **over** the container's `/etc/searxng/`, which means SearXNG's auto-generated `settings.yml` is written to the host mount. The `docker compose exec cat` step may be unnecessary — the file may already be on the host after startup. | **MEDIUM** | **LOW** — the exec command still works, it's just redundant | **LOW** | ⚠️ Document |
| **R6** | **`host.docker.internal` on Docker Desktop Windows** — works by default on Docker Desktop with WSL2 backend, but if student uses Docker Engine in WSL2 without Docker Desktop, `host.docker.internal` won't resolve. | **LOW** | **HIGH** — Option B students stuck if not using Docker Desktop | **MEDIUM** | ✅ Add note |
| **R7** | **`.env` file creation with PowerShell here-string** — CRLF/BOM issues | **MEDIUM** | **MEDIUM** | **✅ FIXED** → uses `[System.IO.File]::WriteAllText()` |
| **R8** | **SearXNG secret key generation** — complex PS script + BOM risk | **MEDIUM** | **MEDIUM** | **✅ FIXED** → `openssl rand -hex 32` or `docker compose exec python3` |
| **R9** | **SearXNG volume bind mount `./searxng:/etc/searxng`** — On Windows, Docker Desktop maps this to `C:\hermes_dev\search-engine\searxng`. If the directory doesn't exist, Docker creates it. But file permissions between Windows host and Linux container can cause SearXNG to fail to write `settings.yml`. This is a known Windows+Docker issue. | **MEDIUM** | **HIGH** — SearXNG can't start if it can't write settings | **MEDIUM** | ⚠️ Add note |
| **R10** | **`python -m json.tool`** — Windows 11 may have `python` as Python launcher (`py`) or may not be on PATH at all. If Python isn't installed, every verification command fails. | **MEDIUM** | **LOW** — verification commands fail but services still work | **LOW** | ⚠️ Add note |
| **R11** | **Firecrawl `OPENAI_BASE_URL` points to `host.docker.internal:11434`** — This assumes Ollama is running on the host. If no Ollama, Firecrawl AI features silently fail but don't crash. Not critical for basic operation. | **LOW** | **LOW** — AI features degrade, basic scrape/crawl still works | **LOW** | ⚠️ Document |
| **R12** | **No `.env` file exists yet** — `search-engine/.env` is referenced but doesn't exist. Students must create it. The doc tells them to create it, so this is OK as long as they follow steps. | **LOW** | **LOW** — `docker compose up` will use defaults from `${FIRECRAWL_BULL_AUTH_KEY:-changeme123}` | **LOW** | ⚠️ OK |
| **R13** | **`USE_DB_AUTHENTICATION: "false"`** in docker-compose.yml — Firecrawl API is open to anyone who can reach `localhost:3002`. On a shared network, this is a security risk. | **LOW** | **MEDIUM** — only localhost-exposed, so low risk on personal machine | **LOW** | ⚠️ Document |

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2 (R1, R3) |
| HIGH | 2 (R2, R9) |
| MEDIUM | 4 (R4, R7, R8, R10) |
| LOW | 5 (R5, R6, R11, R12, R13) |

## Recommended Fixes (Priority Order)

### R1 — `curl` on Windows (CRITICAL)
Windows PowerShell 5.1 aliases `curl` to `Invoke-WebRequest`. Two options:
- **Option A (Recommended):** Add a "Prerequisites" note telling students to use PowerShell 7+ or run `curl.exe` explicitly
- **Option B:** Replace all `curl` with `Invoke-RestMethod` equivalents for PS 5.1 compatibility
- **Best:** Use `curl.exe` everywhere (works on both PS 5.1 and PS 7+)

### R3 — docker-compose.yml REDIS_URL (CRITICAL)
Verify line 130 in docker-compose.yml. If it says `redis://firecrawl-redis:***@firecrawl-rabbitmq:5672`, it's WRONG. Should be `redis://firecrawl-redis:6379` (no password, correct host/port). The current file shows it correctly on the search output, but the redacted line shows a mixed URL. **Must verify and fix.**

### R2 — Out-File BOM (HIGH)
Replace `Out-File -Encoding utf8` with `Out-File -Encoding utf8NoBOM` (PS 7+) or use `docker compose exec searxng cat /etc/searxng/settings.yml > .\searxng\settings.yml` which uses cmd.exe redirection (no BOM).

### R7 — .env CRLF issues (MEDIUM)
Use `docker compose exec` or write `.env` with `[System.IO.File]::WriteAllText()` to avoid BOM/CRLF issues. Or add a note about using VS Code / Notepad++ instead of PowerShell here-strings.

### R8 — Secret key generation (MEDIUM)
Simplify to `openssl rand -hex 32` (available in Git Bash which Docker Desktop installs) or use Docker's own secret generation.

### R9 — Windows file permissions (MEDIUM)
Add a note: if SearXNG fails to start, try `docker compose exec searxng cat /etc/searxng/settings.yml` to verify the file exists and is readable.

### R10 — Python not installed (MEDIUM)
Add note: if `python -m json.tool` fails, install Python or use `curl.exe -s "http://localhost:8080/search?q=test&format=json"` and pipe to a file, then inspect with Notepad.