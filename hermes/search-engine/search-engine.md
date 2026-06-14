# Search Engine Infrastructure — SearXNG + Firecrawl

> **Prerequisite:** Docker Desktop installed and running on Windows 11.
> If you haven't set up Docker yet, complete **[Lab 1, Option 3](../docs/training/Hermes-Beginner-Handbook.md)** first (Docker on Windows 11 / Ubuntu Container), then return here.
>
> **You are here:** This section covers self-hosted web search (SearXNG) and web extraction (Firecrawl) — the two services Hermes needs for `web_search` and `web_extract` to work locally without cloud API keys.

---

## Two Ways to Run Hermes

Students who completed **Lab 1, Option 3** have two Hermes instances available:

| | Option A: Hermes on Windows 11 | Option B: Hermes in Linux Container |
|---|---|---|
| **Where Hermes runs** | Installed directly on Windows | Inside the `hermes-dev` Docker container |
| **How to install** | `curl.exe -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` in PowerShell | Already installed inside container (Lab 1) |
| **Config location** | `C:\Users\<you>\.hermes\` | `/home/thanit/.hermes/` (maps from `C:\hermes_dev\home`) |
| **SearXNG address** | `http://localhost:8080` | `http://host.docker.internal:8080` |
| **Firecrawl address** | `http://localhost:3002` | `http://host.docker.internal:3002` |
| **Qdrant address** | `http://localhost:6333` | `http://host.docker.internal:6333` |

> **Why the difference?** Docker containers on Windows use `host.docker.internal` to reach services on the host. When Hermes itself runs in a container (Option B), it uses `host.docker.internal`. When Hermes runs on Windows directly (Option A), it uses `localhost`.

Both options share the **same Docker containers** for SearXNG, Firecrawl, and Qdrant — they always run on the Windows host.

---

## What You Get

| Service | Purpose | Windows Host Port | Container Port |
|---------|---------|-------------------|----------------|
| **SearXNG** | Meta-search engine (Google, Bing, DuckDuckGo, etc.) | `localhost:8080` | `8080` |
| **Firecrawl** | Web crawling, JavaScript rendering, structured extraction | `localhost:3002` | `3002` |
| **Qdrant** | Vector similarity database (`fact_store`, skills) | `localhost:6333` | `6333` |

All three run in Docker with **zero external API keys required** for basic operation.

## Directory Structure

Before you run any commands, create the folder layout below. Everything lives under `C:\hermes_dev\search-engine\`:

```
C:\hermes_dev\search-engine\
├── docker-compose.yml          # Full stack definition (SearXNG + Firecrawl + Qdrant)
├── .env                        # Secrets: BULL_AUTH_KEY, AI model names (NEVER commit to git)
├── searxng\                    # SearXNG config volume (mounted into container)
│   └── settings.yml            # Search engines list + JSON format toggle
├── qdrant-data\                # Vector DB persistence (survives container restarts)
└── firecrawl-pgdata\           # Firecrawl PostgreSQL data
```

**What each file does:**

| File / Folder | Purpose | Who creates it |
|---|---|---|
| `docker-compose.yml` | Defines all 8 Docker services, ports, volumes, memory limits | **You** — copy from this guide |
| `.env` | Holds secrets (`FIRECRAWL_BULL_AUTH_KEY`, model names) | **You** — Step 2 below |
| `searxng/` | Live SearXNG configuration; edits on Windows propagate into container | **Docker** — auto-created on first run |
| `qdrant-data/` | Persistent vector storage for embeddings | **Docker** — auto-created on first run |
| `firecrawl-pgdata/` | Firecrawl job queue and crawl history | **Docker** — auto-created on first run |

> **Security rule:** Only `docker-compose.yml` and `.env` are human-edited. The three data folders are managed by Docker — do not delete them unless you want to wipe all search history and vector data.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Windows 11 Host                            │
│                                                              │
│  ┌─────────────┐   web_search    ┌──────────┐              │
│  │   Hermes    │ ──────────────→ │ SearXNG  │              │
│  │   Agent     │  localhost:8080   │  :8080   │──→ Internet │
│  │             │  or              │          │              │
│  │             │  host.docker.     └──────────┘              │
│  │             │  internal:8080                              │
│  │             │                                              │
│  │             │   web_extract   ┌──────────────────┐      │
│  │             │ ──────────────→ │ Firecrawl API    │      │
│  │             │  localhost:3002 │  :3002            │      │
│  │             │  or              │   ┌─────────┐    │      │
│  │             │  host.docker.    │   │Playwright│   │──→ Web │
│  │             │  internal:3002   │   │  :3000   │   │      │
│  │             │                  │   │Redis│PgSQL│  │      │
│  │             │                  └──────────────────┘      │
│  │             │                                              │
│  │             │   fact_store    ┌──────────┐              │
│  │             │ ──────────────→ │ Qdrant   │              │
│  │             │  localhost:6333 │  :6333   │              │
│  │             │  or              └──────────┘              │
│  │             │  host.docker.                               │
│  │             │  internal:6333                              │
│  └─────────────┘                                           │
│                                                              │
│  ┌───────────────────────────────────────────┐               │
│  │  hermes-dev Linux container (Option B)    │               │
│  │  Volume: C:\hermes_dev\home → /home/thanit│               │
│  └───────────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

Hermes calls `web_search` → SearXNG queries multiple search engines → returns aggregated JSON results.
Hermes calls `web_extract` → Firecrawl fetches the URL, renders JavaScript if needed → returns clean markdown.

---

## Quick Start (5 minutes)

All commands below run in **PowerShell** on Windows 11.

### 1. Navigate to the search-engine directory

```powershell
cd C:\hermes_dev\search-engine
dir
# You should see: docker-compose.yml  searxng\  firecrawl-pgdata\
```

### 2. Create the `.env` file

```powershell
cd C:\hermes_dev\search-engine

$envContent = @"
# -- Firecrawl self-hosted -----------------------------------------
# No external API key needed. This key is only for the admin UI:
# http://localhost:3002/admin/<KEY>/queues
FIRECRAWL_BULL_AUTH_KEY=changeme-to-a-random-secret

# -- Firecrawl AI features (optional) -------------------------------
# Uncomment and fill in if you want better extraction quality.
# Uses your existing Ollama Cloud Pro key:
FIRECRAWL_MODEL_NAME=glm-5.1:cloud
FIRECRAWL_EMBED_MODEL=nomic-embed-text
"@
[System.IO.File]::WriteAllText("$PWD\.env", $envContent)
```

> **Security note:** The `.env` file contains secrets. Never commit it to git. Add `.env` to `.gitignore`.

### 3. Create the `docker-compose.yml` file

Create `C:\hermes_dev\search-engine\docker-compose.yml` with the full content below. Every line is explained in the **Key lines** table after it.

```yaml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    restart: unless-stopped
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/

  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "127.0.0.1:6333:6333"
      - "127.0.0.1:6334:6334"
    volumes:
      - ./qdrant-data:/qdrant/storage
    restart: unless-stopped

  # ── Firecrawl (self-hosted) ───────────────────────────────────────────
  # Provides web_extract for Hermes: crawling, structured extraction,
  # and JavaScript-rendered page content. Paired with SearXNG for search.
  #
  # Requires a .env file in this directory with:
  #   FIRECRAWL_BULL_AUTH_KEY=<random-secret>   (admin UI password)
  #
  # API endpoint: http://localhost:3002
  # Admin UI:     http://localhost:3002/admin/<BULL_AUTH_KEY>/queues
  #
  # ── 8 GB VPS: concurrency limits ─────────────────────────────────────
  # With only ~8 GB total RAM, Playwright (Chromium) is the main risk.
  # Each tab uses ~200–400 MB; unthrottled, 10 concurrent crawls can OOM
  # the host.  The settings below cap Firecrawl to 1–2 concurrent crawls
  # and keep total Firecrawl RAM under ~4 GB:
  #
  #   firecrawl-api        → 4 GB limit  (API + worker processes)
  #   firecrawl-playwright → 2 GB limit  (headless Chromium tabs)
  #   NUM_WORKERS_PER_QUEUE=2   max parallel workers per queue
  #   CRAWL_CONCURRENT_REQUESTS=2  max in-flight crawl HTTP requests
  #   MAX_CONCURRENT_JOBS=2   max simultaneous crawl/scrape jobs
  #   BROWSER_POOL_SIZE=2   headless browser instances kept warm
  #   MAX_CONCURRENT_PAGES=2  tabs per Playwright container
  #   MAX_RAM=0.8   reject new jobs when RAM > 80% of container limit
  #   MAX_CPU=0.8   reject new jobs when CPU > 80%
  #
  # To raise throughput: increase all *2* values to 3 or 4, bump the
  # Playwright memory limit to 3–4 GB, and raise the API limit to match.
  # ──────────────────────────────────────────────────────────────────────

  firecrawl-api:
    image: ghcr.io/firecrawl/firecrawl:latest
    container_name: firecrawl-api
    restart: unless-stopped
    ports:
      - "127.0.0.1:3002:3002"
    environment:
      HOST: "0.0.0.0"
      PORT: 3002
      # ── concurrency limits (tuned for 8 GB host) ──
      NUM_WORKERS_PER_QUEUE: "2"
      CRAWL_CONCURRENT_REQUESTS: "2"
      MAX_CONCURRENT_JOBS: "2"
      BROWSER_POOL_SIZE: "2"
      MAX_CPU: "0.8"
      MAX_RAM: "0.8"
      REDIS_URL: redis://firecrawl-redis:6379
      BULL_AUTH_KEY: ${FIRECRAWL_BULL_AUTH_KEY:-changeme123}
      USE_DB_AUTHENTICATION: "false"
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
      POSTGRES_HOST: firecrawl-postgres
      POSTGRES_PORT: "5432"
      # AI features — point at Ollama Cloud Pro for /extract and /scrape with LLM
      OPENAI_BASE_URL: http://host.docker.internal:11434/v1
      MODEL_NAME: ${FIRECRAWL_MODEL_NAME:-glm-5.1:cloud}
      MODEL_EMBEDDING_NAME: ${FIRECRAWL_EMBED_MODEL:-nomic-embed-text}
      # SearXNG integration — reuse your existing instance for /search
      SEARXNG_ENDPOINT: http://searxng:8080
    depends_on:
      firecrawl-redis:
        condition: service_started
      firecrawl-playwright:
        condition: service_started
      firecrawl-rabbitmq:
        condition: service_healthy
    extra_hosts:
      - "host.docker.internal:host-gateway"
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G

  firecrawl-playwright:
    image: ghcr.io/firecrawl/playwright-service:latest
    container_name: firecrawl-playwright
    restart: unless-stopped
    environment:
      PORT: 3000
      BLOCK_MEDIA: "false"
      MAX_CONCURRENT_PAGES: "2"
    deploy:
      resources:
        limits:
          cpus: "1.5"
          memory: 2G
    tmpfs:
      - /tmp/.cache:noexec,nosuid,size=512m

  firecrawl-redis:
    image: redis:alpine
    container_name: firecrawl-redis
    restart: unless-stopped
    command: redis-server --bind 0.0.0.0 --maxmemory 256mb --maxmemory-policy allkeys-lru
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

  firecrawl-rabbitmq:
    image: rabbitmq:3-management
    container_name: firecrawl-rabbitmq
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: firecrawl
      RABBITMQ_DEFAULT_PASS: firecrawl
    volumes:
      - firecrawl-rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "check_running"]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  firecrawl-postgres:
    image: ghcr.io/firecrawl/nuq-postgres:latest
    container_name: firecrawl-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    volumes:
      - ./firecrawl-pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

volumes:
  firecrawl-rabbitmq-data:
```

**Key lines to study in the compose file above:**

| Line | What it does | Why it matters |
|---|---|---|
| `OPENAI_BASE_URL: http://host.docker.internal:11434/v1` | Routes Firecrawl's LLM calls to your host Ollama daemon | `host.docker.internal` lets the container reach the host machine — this is how Firecrawl talks to Ollama Cloud Pro |
| `MODEL_NAME: ${FIRECRAWL_MODEL_NAME:-glm-5.1:cloud}` | Uses your `.env` value, falls back to `glm-5.1:cloud` | The `:cloud` tag tells Ollama to route to Cloud Pro instead of running locally |
| `MODEL_EMBEDDING_NAME: ${FIRECRAWL_EMBED_MODEL:-nomic-embed-text}` | Embedding model for vector extraction | Embeddings run locally — small enough, no cloud round-trip needed |
| `SEARXNG_ENDPOINT: http://searxng:8080` | Connects Firecrawl's `/search` to SearXNG | Docker internal DNS — `searxng` resolves to the SearXNG container |
| `depends_on:` with `condition:` | Ensures Redis, Playwright, and RabbitMQ start before the API | Prevents crash-loop on startup |
| `host.docker.internal:host-gateway` | Maps the Docker gateway to `host.docker.internal` | Required on Windows Docker Desktop so containers can reach the host's Ollama |
| `127.0.0.1:` on all ports | Binds to localhost only | Prevents external access — only your machine can reach these services |

### 4. Start All Services

```powershell
cd C:\hermes_dev\search-engine
docker compose up -d
```

First run pulls images (~2 GB total). Subsequent starts are instant.

### 4. Configure SearXNG JSON Output (REQUIRED)

SearXNG blocks JSON API queries by default. You **must** enable JSON format before Hermes can use it:

```powershell
cd C:\hermes_dev\search-engine

# Start SearXNG briefly to generate settings.yml
docker compose up -d searxng
Start-Sleep -Seconds 10
docker compose stop searxng

# Copy the generated settings to your local volume
# Copy settings without BOM (Out-File -Encoding utf8 adds BOM which corrupts YAML)
$settings = docker compose exec searxng cat /etc/searxng/settings.yml
[System.IO.File]::WriteAllText("$PWD\searxng\settings.yml", $settings)
```

Now edit `C:\hermes_dev\search-engine\searxng\settings.yml`. Find the `search:` section and add `json` to `formats`:

```yaml
search:
  safe_search: 0
  autocomplete: ""
  default_lang: "en"
  formats:
    - html
    - json                 # <-- ADD THIS LINE. Without it, web_search returns 403!
```

Also generate a secret key:

```powershell
# Generate a random secret key (use Git Bash which comes with Docker Desktop)
openssl rand -hex 32
# Copy the output and paste it as the secret_key value in settings.yml
```

Or generate it directly inside the SearXNG container:

```powershell
docker compose exec searxng python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy the output and paste it as the secret_key value in settings.yml
```

Now start all services:

```powershell
docker compose up -d
```

> ⚠️ **If you skip the `formats: json` step, every Hermes `web_search` call will fail with a 403 error.** This is the #1 setup mistake.

### 5. Verify Everything Is Running

```powershell
# Check all containers are "Up"
docker compose ps

# Test SearXNG -- MUST return JSON, not HTML or 403
curl.exe -s "http://localhost:8080/search?q=test&format=json" | python -m json.tool | Select-Object -First 20

# If the above returns HTML or "403 Forbidden", go back to Step 4 and ensure
# `json` is in the `formats:` list in searxng\settings.yml, then restart.

# Test Firecrawl
curl.exe -s -X POST http://localhost:3002/v1/scrape `
  -H "Content-Type: application/json" `
  -d '{"url": "https://example.com"}' | python -m json.tool | Select-Object -First 20

# Test Qdrant
curl.exe -s http://localhost:6333/collections | python -m json.tool
```

Expected results:
- **SearXNG:** JSON with `results` array containing search hits
- **Firecrawl:** JSON with `markdown` or `content` field containing page text
- **Qdrant:** JSON with `result.collections` list (may be empty — that's OK)

If any test fails, see [Troubleshooting](#troubleshooting) below.

---

## Service Details

### SearXNG (Web Search)

**What it does:** Aggregates results from Google, Bing, DuckDuckGo, Wikipedia, and 70+ other engines. Returns clean JSON that Hermes parses via `web_search`.

**Configuration directory:** `C:\hermes_dev\search-engine\searxng\`

On first start, SearXNG creates default settings. You **must** customize it to enable JSON output — without this, Hermes `web_search` will fail with 403 errors.

#### Step 1: Generate the default settings

```powershell
cd C:\hermes_dev\search-engine
docker compose up -d searxng
Start-Sleep -Seconds 10
docker compose stop searxng

# Copy settings without BOM (Out-File -Encoding utf8 adds BOM which corrupts YAML)
$settings = docker compose exec searxng cat /etc/searxng/settings.yml
[System.IO.File]::WriteAllText("$PWD\searxng\settings.yml", $settings)
```

#### Step 2: Enable JSON format (CRITICAL)

**SearXNG defaults to HTML-only output.** If you skip this step, `web_search` will return 403 Forbidden errors.

Open `C:\hermes_dev\search-engine\searxng\settings.yml` and find the `search:` section. Add `json` to the `formats:` list:

```yaml
# C:\hermes_dev\search-engine\searxng\settings.yml

use_default_settings: true

search:
  safe_search: 0          # 0=off, 1=moderate, 2=strict
  autocomplete: ""        # Disable autocomplete for API use
  default_lang: "en"      # Default search language
  formats:
    - html
    - json                 # <-- CRITICAL: Required for Hermes web_search!
```

If the `formats:` key doesn't exist yet, add it under `search:`. If it only lists `- html`, add `- json` on the next line.

> ⚠️ **Without `json` in the formats list, SearXNG will:**
> - Return **403 Forbidden** when Hermes calls `http://localhost:8080/search?q=...&format=json`
> - Return **HTML** instead of JSON for curl.exe tests
> - Silently break all `web_search` tool calls in Hermes

#### Step 3: Tune remaining settings

While you have `settings.yml` open, verify these values:

```yaml
server:
  secret_key: "change-this-to-a-random-string"  # Required! Generate with PowerShell:
  bind_address: "0.0.0.0"
  port: 8080
  limiter: false           # Disable rate limiter for local use

outgoing:
  request_timeout: 10.0    # Seconds before timeout
  useragent_suffix: ""      # Append to default user agent

engines:
  - name: google
    engine: google
    shortcut: g

  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg

  - name: wikipedia
    engine: wikipedia
    shortcut: wp
```

#### Step 4: Restart SearXNG with new settings

```powershell
docker compose up -d searxng
```

#### Step 5: Verify JSON output works

```powershell
# This MUST return JSON, not HTML or a 403 error
curl.exe -s "http://localhost:8080/search?q=test&format=json" | python -m json.tool | Select-Object -First 20
```

If you see a JSON object with a `"results"` array, SearXNG is correctly configured. If you see HTML or a 403 error, go back to **Step 2** and make sure `json` is in the `formats:` list.

**Additional SearXNG test queries:**

```powershell
# Search with categories
curl.exe -s "http://localhost:8080/search?q=Windows+11+terminal+tricks&format=json&categories=general,it" | python -m json.tool

# Search specific engine
curl.exe -s "http://localhost:8080/search?q=python+async&format=json&engines=google,duckduckgo" | python -m json.tool
```

### Firecrawl (Web Extraction)

**What it does:** Fetches any URL, renders JavaScript with headless Chromium, and returns clean markdown. Handles dynamic pages (SPAs, charts, login-protected content) that simple `curl` cannot.

**Architecture:** Firecrawl runs 5 containers:
- `firecrawl-api` — The main API server (port 3002)
- `firecrawl-playwright` — Headless Chromium for JS rendering
- `firecrawl-redis` — Job queue cache
- `firecrawl-rabbitmq` — Message broker for job distribution
- `firecrawl-postgres` — Persistent storage

**Memory limits** (tuned for an 8 GB VPS; raise for 16 GB machines):

| Container | CPU Limit | Memory Limit | Purpose |
|-----------|-----------|-------------|---------|
| firecrawl-api | 2.0 | 4 GB | API + worker processes |
| firecrawl-playwright | 1.5 | 2 GB | Headless Chromium tabs |
| firecrawl-redis | 0.5 | 512 MB | Queue cache |
| firecrawl-rabbitmq | 1.0 | 512 MB | Message broker |
| firecrawl-postgres | 0.5 | 512 MB | Database |

> **For 16 GB machines:** You can safely raise `MAX_CONCURRENT_JOBS`, `BROWSER_POOL_SIZE`, and `MAX_CONCURRENT_PAGES` from 2 to 4, and increase Playwright memory to 4 GB in `docker-compose.yml`.

<details>
<summary>📄 Full <code>docker-compose.yml</code> — click to expand</summary>

```yaml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    restart: unless-stopped
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/

  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "127.0.0.1:6333:6333"
      - "127.0.0.1:6334:6334"
    volumes:
      - ./qdrant-data:/qdrant/storage
    restart: unless-stopped

  # ── Firecrawl (self-hosted) ───────────────────────────────────────────
  # Provides web_extract for Hermes: crawling, structured extraction,
  # and JavaScript-rendered page content. Paired with SearXNG for search.
  #
  # Requires a .env file in this directory with:
  #   FIRECRAWL_BULL_AUTH_KEY=<random-secret>   (admin UI password)
  #
  # API endpoint: http://localhost:3002
  # Admin UI:     http://localhost:3002/admin/<BULL_AUTH_KEY>/queues
  #
  # ── 8 GB VPS: concurrency limits ─────────────────────────────────────
  # With only ~8 GB total RAM, Playwright (Chromium) is the main risk.
  # Each tab uses ~200–400 MB; unthrottled, 10 concurrent crawls can OOM
  # the host.  The settings below cap Firecrawl to 1–2 concurrent crawls
  # and keep total Firecrawl RAM under ~4 GB:
  #
  #   firecrawl-api        → 4 GB limit  (API + worker processes)
  #   firecrawl-playwright → 2 GB limit  (headless Chromium tabs)
  #   NUM_WORKERS_PER_QUEUE=2   max parallel workers per queue
  #   CRAWL_CONCURRENT_REQUESTS=2  max in-flight crawl HTTP requests
  #   MAX_CONCURRENT_JOBS=2   max simultaneous crawl/scrape jobs
  #   BROWSER_POOL_SIZE=2   headless browser instances kept warm
  #   MAX_CONCURRENT_PAGES=2  tabs per Playwright container
  #   MAX_RAM=0.8   reject new jobs when RAM > 80% of container limit
  #   MAX_CPU=0.8   reject new jobs when CPU > 80%
  #
  # To raise throughput: increase all *2* values to 3 or 4, bump the
  # Playwright memory limit to 3–4 GB, and raise the API limit to match.
  # ──────────────────────────────────────────────────────────────────────

  firecrawl-api:
    image: ghcr.io/firecrawl/firecrawl:latest
    container_name: firecrawl-api
    restart: unless-stopped
    ports:
      - "127.0.0.1:3002:3002"
    environment:
      HOST: "0.0.0.0"
      PORT: 3002
      # ── concurrency limits (tuned for 8 GB host) ──
      NUM_WORKERS_PER_QUEUE: "2"
      CRAWL_CONCURRENT_REQUESTS: "2"
      MAX_CONCURRENT_JOBS: "2"
      BROWSER_POOL_SIZE: "2"
      MAX_CPU: "0.8"
      MAX_RAM: "0.8"
      REDIS_URL: redis://firecrawl-redis:6379
      REDIS_RATE_LIMIT_URL: redis://firecrawl-redis:6379
      NUQ_RABBITMQ_URL: amqp://firecrawl:firecrawl@firecrawl-rabbitmq:5672
      BULL_AUTH_KEY: ${FIRECRAWL_BULL_AUTH_KEY:-changeme123}
      USE_DB_AUTHENTICATION: "false"
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
      POSTGRES_HOST: firecrawl-postgres
      POSTGRES_PORT: "5432"
      # AI features — point at Ollama Cloud Pro for /extract and /scrape with LLM
      OPENAI_BASE_URL: http://host.docker.internal:11434/v1
      MODEL_NAME: ${FIRECRAWL_MODEL_NAME:-glm-5.1:cloud}
      MODEL_EMBEDDING_NAME: ${FIRECRAWL_EMBED_MODEL:-nomic-embed-text}
      # SearXNG integration — reuse your existing instance for /search
      SEARXNG_ENDPOINT: http://searxng:8080
    depends_on:
      firecrawl-redis:
        condition: service_started
      firecrawl-playwright:
        condition: service_started
      firecrawl-rabbitmq:
        condition: service_healthy
    extra_hosts:
      - "host.docker.internal:host-gateway"
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G

  firecrawl-playwright:
    image: ghcr.io/firecrawl/playwright-service:latest
    container_name: firecrawl-playwright
    restart: unless-stopped
    environment:
      PORT: 3000
      BLOCK_MEDIA: "false"
      MAX_CONCURRENT_PAGES: "2"
    deploy:
      resources:
        limits:
          cpus: "1.5"
          memory: 2G
    tmpfs:
      - /tmp/.cache:noexec,nosuid,size=512m

  firecrawl-redis:
    image: redis:alpine
    container_name: firecrawl-redis
    restart: unless-stopped
    command: redis-server --bind 0.0.0.0 --maxmemory 256mb --maxmemory-policy allkeys-lru
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

  firecrawl-rabbitmq:
    image: rabbitmq:3-management
    container_name: firecrawl-rabbitmq
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: firecrawl
      RABBITMQ_DEFAULT_PASS: firecrawl
    volumes:
      - firecrawl-rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "check_running"]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  firecrawl-postgres:
    image: ghcr.io/firecrawl/nuq-postgres:latest
    container_name: firecrawl-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    volumes:
      - ./firecrawl-pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

volumes:
  firecrawl-rabbitmq-data:
```

</details>

**Key lines to study in the compose file above:**

| Line | What it does | Why it matters |
|---|---|---|
| `OPENAI_BASE_URL: http://host.docker.internal:11434/v1` | Routes Firecrawl's LLM calls to your host Ollama daemon | `host.docker.internal` lets the container reach the host machine — this is how Firecrawl talks to Ollama Cloud Pro |
| `MODEL_NAME: ${FIRECRAWL_MODEL_NAME:-glm-5.1:cloud}` | Uses your `.env` value, falls back to `glm-5.1:cloud` | The `:cloud` tag tells Ollama to route to Cloud Pro instead of running locally |
| `MODEL_EMBEDDING_NAME: ${FIRECRAWL_EMBED_MODEL:-nomic-embed-text}` | Embedding model for vector extraction | Embeddings run locally — small enough, no cloud round-trip needed |
| `SEARXNG_ENDPOINT: http://searxng:8080` | Connects Firecrawl's `/search` to SearXNG | Docker internal DNS — `searxng` resolves to the SearXNG container |
| `depends_on:` with `condition:` | Ensures Redis, Playwright, and RabbitMQ start before the API | Prevents crash-loop on startup |
| `host.docker.internal:host-gateway` | Maps the Docker gateway to `host.docker.internal` | Required on Windows Docker Desktop so containers can reach the host's Ollama |
| `127.0.0.1:` on all ports | Binds to localhost only | Prevents external access — only your machine can reach these services |

**Firecrawl AI features (optional):** Set `FIRECRAWL_MODEL_NAME` and `FIRECRAWL_EMBED_MODEL` in `.env` to enable LLM-powered extraction. These point at your Ollama Cloud instance:

```env
# In .env -- reuses your existing Ollama Cloud key
FIRECRAWL_MODEL_NAME=glm-5.1:cloud      # GLM-5.1 on Ollama Cloud Pro
FIRECRAWL_EMBED_MODEL=nomic-embed-text      # Embedding model
```

> **How it works:** `docker-compose.yml` already routes `OPENAI_BASE_URL` to your host Ollama instance:
> ```yaml
> OPENAI_BASE_URL: http://host.docker.internal:11434/v1   # Points to host Ollama
> ```
> When you set `FIRECRAWL_MODEL_NAME=glm-5.1:cloud`, Firecrawl sends `/extract` and `/scrape` LLM requests through this URL to your Ollama daemon, which forwards `:cloud`-tagged models to Ollama Cloud Pro using the `OLLAMA_API_KEY` from your `~/.hermes/.env`. The embedding model (`nomic-embed-text`) runs locally because embeddings are small and fast — no cloud round-trip needed.

**Testing Firecrawl manually:**

```powershell
# Simple scrape
curl.exe -s -X POST http://localhost:3002/v1/scrape `
  -H "Content-Type: application/json" `
  -d '{"url": "https://news.ycombinator.com"}' | python -m json.tool

# Crawl (follows links within a domain)
curl.exe -s -X POST http://localhost:3002/v1/crawl `
  -H "Content-Type: application/json" `
  -d '{"url": "https://example.com", "limit": 5}' | python -m json.tool

# Extract structured data
curl.exe -s -X POST http://localhost:3002/v1/extract `
  -H "Content-Type: application/json" `
  -d '{"urls": ["https://example.com"], "prompt": "Extract the main heading and first paragraph"}' | python -m json.tool
```

**Admin UI:** `http://localhost:3002/admin/<YOUR_FIRECRAWL_BULL_AUTH_KEY>/queues`

### Qdrant (Vector Database)

**What it does:** Stores vector embeddings for Hermes' `fact_store` and skill search. Qdrant runs on port 6333 (gRPC) and 6334 (REST).

**Data persistence:** Stored in `C:\hermes_dev\search-engine\qdrant-data\`. This directory survives container restarts.

**Testing Qdrant:**

```powershell
# Check collections
curl.exe http://localhost:6333/collections | python -m json.tool

# Create a test collection
curl.exe -s -X PUT http://localhost:6333/collections/test `
  -H "Content-Type: application/json" `
  -d '{"vectors": {"size": 4, "distance": "Cosine"}}' | python -m json.tool

# Delete the test collection
curl.exe -s -X DELETE http://localhost:6333/collections/test | python -m json.tool
```

---

## Configuring Hermes to Use These Services

### Option A: Hermes on Windows 11

Use `localhost` for all service addresses.

#### Step 1: Edit Hermes config

```powershell
# Open config in your editor
notepad C:\Users\$env:USERNAME\.hermes\config.yaml
```

Add or verify these lines:

```yaml
web:
  search_backend: searxng     # Use SearXNG for web_search
  extract_backend: firecrawl  # Use Firecrawl for web_extract

web_search:
  provider: searxng
  url: http://localhost:8080   # SearXNG URL

browser:
  inactivity_timeout: 120
  command_timeout: 30
```

#### Step 2: Edit Hermes `.env`

```powershell
notepad C:\Users\$env:USERNAME\.hermes\.env
```

Add or verify these lines:

```env
# SearXNG -- self-hosted web search
SEARXNG_URL=http://127.0.0.1:8080

# Firecrawl -- self-hosted web extraction (no API key needed)
FIRECRAWL_API_URL=http://localhost:3002
```

> **Note:** `FIRECRAWL_API_URL` (not `FIRECRAWL_API_KEY`) is used for self-hosted Firecrawl. When `USE_DB_AUTHENTICATION=false` in docker-compose.yml, no API key is required.

#### Step 3: Restart Hermes

```powershell
# If running in TUI mode, exit and restart
hermes --tui
```

#### Step 4: Verify in Hermes

Inside a Hermes chat session, test both tools:

```
# Test web_search (uses SearXNG)
Use web_search to find the latest news about Windows 12.

# Test web_extract (uses Firecrawl)
Use web_extract to get the full content of https://example.com and summarize it.
```

If both return real results, your search infrastructure is fully configured.

---

### Option B: Hermes in Linux Container

Use `host.docker.internal` for all service addresses — Docker containers use this to reach the host.

#### Step 1: SSH into the container

```powershell
ssh thanit@localhost -p 2222
```

#### Step 2: Edit Hermes config

```bash
nano /home/thanit/.hermes/config.yaml
```

Add or verify these lines:

```yaml
web:
  search_backend: searxng     # Use SearXNG for web_search
  extract_backend: firecrawl  # Use Firecrawl for web_extract

web_search:
  provider: searxng
  url: http://host.docker.internal:8080   # SearXNG via Docker host

browser:
  inactivity_timeout: 120
  command_timeout: 30
```

#### Step 3: Edit Hermes `.env`

```bash
nano /home/thanit/.hermes/.env
```

Add or verify these lines:

```env
# SearXNG -- self-hosted web search
SEARXNG_URL=http://host.docker.internal:8080

# Firecrawl -- self-hosted web extraction (no API key needed)
FIRECRAWL_API_URL=http://host.docker.internal:3002
```

> **Why `host.docker.internal`?** The Hermes container and the SearXNG/Firecrawl/Qdrant containers are **separate Docker networks**. The Hermes container reaches the host (where SearXNG/Firecrawl/Qdrant are published) via `host.docker.internal`.

#### Step 4: Restart Hermes

```bash
# If running in TUI mode, exit and restart
hermes --tui
```

#### Step 5: Verify in Hermes

Inside a Hermes chat session, test both tools:

```
# Test web_search (uses SearXNG)
Use web_search to find the latest news about Windows 12.

# Test web_extract (uses Firecrawl)
Use web_extract to get the full content of https://example.com and summarize it.
```

If both return real results, your search infrastructure is fully configured.

---

## Resource Usage

| Service | RAM (typical) | RAM (peak) | CPU (idle) | CPU (crawling) |
|---------|---------------|------------|------------|----------------|
| SearXNG | ~80 MB | ~200 MB | <1% | 5-15% |
| Firecrawl API | ~300 MB | ~1 GB | <1% | 10-30% |
| Firecrawl Playwright | ~200 MB | ~1.5 GB | 0% | 20-50% |
| Firecrawl Redis | ~10 MB | ~50 MB | <1% | <1% |
| Firecrawl RabbitMQ | ~50 MB | ~200 MB | <1% | 5% |
| Firecrawl PostgreSQL | ~30 MB | ~200 MB | <1% | 5% |
| Qdrant | ~50 MB | ~500 MB | <1% | 10-30% |
| **Total** | **~720 MB** | **~3.6 GB** | **~5%** | **~50-130%** |

On a 16 GB machine, this leaves ~12 GB for Hermes, Windows, and browser — plenty of headroom.

> **Tip:** If you're not using Firecrawl's extraction features, you can stop just those containers:
> ```powershell
> docker compose stop firecrawl-api firecrawl-playwright firecrawl-redis firecrawl-rabbitmq firecrawl-postgres
> ```
> This saves ~1 GB of RAM while keeping SearXNG and Qdrant running.

---

## Troubleshooting

### ⚠️ SearXNG returns 403 Forbidden or HTML instead of JSON (MOST COMMON)

This is the **#1 setup mistake**. SearXNG blocks JSON API queries by default.

```powershell
# If this returns HTML or 403 instead of JSON:
curl.exe -s "http://localhost:8080/search?q=test&format=json" | Select-Object -First 5

# Fix: edit C:\hermes_dev\search-engine\searxng\settings.yml and ensure formats includes json:
#   search:
#     formats:
#       - html
#       - json    <-- THIS LINE IS REQUIRED
#
# Then restart:
docker compose restart searxng

# Verify it now returns JSON:
curl.exe -s "http://localhost:8080/search?q=test&format=json" | python -m json.tool | Select-Object -First 5
```

If you still get 403 after adding `json` to formats, also add `enable_http: true` under `outgoing:`:

```yaml
outgoing:
  enable_http: true    # Allow HTTP (not just HTTPS) for outgoing requests
```

### SearXNG returns empty results

```powershell
# Check SearXNG logs
docker compose logs searxng --tail 50

# Common issue: rate limiting by search engines
# Fix: edit searxng\settings.yml and set:
#   server.limiter: false
# Then restart:
docker compose restart searxng

# Test directly
curl.exe "http://localhost:8080/search?q=test&format=json" | python -m json.tool
```

### Firecrawl returns errors or timeouts

```powershell
# Check Firecrawl logs
docker compose logs firecrawl-api --tail 50

# Common issue: Playwright container not ready
docker compose logs firecrawl-playwright --tail 20

# Fix: restart Playwright
docker compose restart firecrawl-playwright

# Test directly
curl.exe -s -X POST http://localhost:3002/v1/scrape `
  -H "Content-Type: application/json" `
  -d '{"url": "https://example.com"}' | python -m json.tool
```

### Qdrant connection refused

```powershell
# Check Qdrant is running
docker compose ps qdrant

# Check Qdrant logs
docker compose logs qdrant --tail 20

# Test directly
curl.exe http://localhost:6333/collections
```

### Port already in use

```powershell
# Find what's using a port (run in PowerShell)
netstat -ano | findstr :8080   # SearXNG
netstat -ano | findstr :3002   # Firecrawl
netstat -ano | findstr :6333   # Qdrant

# Kill the conflicting process or change the port in docker-compose.yml
```

### Docker compose won't start

```powershell
cd C:\hermes_dev\search-engine

# Full reset (keeps data volumes)
docker compose down
docker compose up -d

# Nuclear option (deletes data volumes too)
docker compose down -v
docker compose up -d
```

### Hermes says "web_search failed" or "web_extract failed"

```powershell
# 1. Verify services are running
docker compose ps

# 2. Test endpoints directly
curl.exe "http://localhost:8080/search?q=test&format=json" | Select-Object -First 5
curl.exe -s -X POST http://localhost:3002/v1/scrape `
  -H "Content-Type: application/json" `
  -d '{"url": "https://example.com"}' | Select-Object -First 5

# 3. Check Hermes config (Option A: Windows)
hermes config show | Select-String "search_backend|extract_backend"

# 3. Check Hermes config (Option B: Linux container)
hermes config show | grep -A3 "search_backend\|extract_backend"

# 4. Check .env has the right URLs
# Option A: Windows
Select-String "SEARXNG_URL|FIRECRAWL_API_URL" C:\Users\$env:USERNAME\.hermes\.env

# Option B: Linux container
grep -i "SEARXNG_URL\|FIRECRAWL_API_URL" /home/thanit/.hermes/.env

# 5. Restart Hermes after config changes
hermes --tui
```

---

## Stopping and Cleaning Up

```powershell
cd C:\hermes_dev\search-engine

# Stop all services (keeps data)
docker compose stop

# Stop and remove containers (keeps data volumes)
docker compose down

# Nuclear: remove everything including data
docker compose down -v
Remove-Item -Recurse -Force qdrant-data, firecrawl-pgdata
```

> **Warning:** `docker compose down -v` deletes all Qdrant vectors, Firecrawl job history, and PostgreSQL data. Only use this if you want a clean slate.

---

## Docker Compose Reference

The full `docker-compose.yml` in this directory defines these services:

| Service | Image | Port(s) | Purpose |
|---------|-------|---------|---------|
| `searxng` | `searxng/searxng:latest` | `127.0.0.1:8080` | Web meta-search |
| `qdrant` | `qdrant/qdrant:latest` | `127.0.0.1:6333, 6334` | Vector database |
| `firecrawl-api` | `ghcr.io/firecrawl/firecrawl:latest` | `127.0.0.1:3002` | Web extraction API |
| `firecrawl-playwright` | `ghcr.io/firecrawl/playwright-service:latest` | internal | Headless Chromium |
| `firecrawl-redis` | `redis:alpine` | internal | Job queue cache |
| `firecrawl-rabbitmq` | `rabbitmq:3-management` | internal | Message broker |
| `firecrawl-postgres` | `ghcr.io/firecrawl/nuq-postgres:latest` | internal | Persistent storage |

> Only SearXNG, Firecrawl, and Qdrant are required for Hermes `web_search`/`web_extract`. The compose file contains only these services.

---

**⬆️ [Back to Table of Contents](../docs/training/Hermes-Beginner-Handbook.md#table-of-contents)**