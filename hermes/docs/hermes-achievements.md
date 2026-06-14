# Hermes Achievements — Complete Reference Catalog

> **Source:** Grok conversation research (X.com share) cross-referenced with official Hermes docs and the `hermes-achievements` GitHub repository.
> **Last updated:** June 2026

---

## What Is Hermes Achievements?

**Hermes Achievements** is a built-in dashboard plugin in **Hermes Agent** (open-source, self-improving AI agent by Nous Research). It adds a **Steam-style achievements system** with **60+ collectible, tiered badges** earned automatically from your real session history.

It gamifies your usage by tracking behaviors like tool chains, debugging, skill/memory usage, model/provider variety, vibe-coding, cron jobs, web research, and lifestyle patterns (e.g., weekend/night sessions). **No manual claiming** — badges unlock based on what you (and your agent) actually do.

---

## Access

Run the Hermes dashboard:

```bash
hermes dashboard
```

Navigate to the **Achievements tab**. You'll see:
- All ~60+ badges (unlocked, discovered, secret)
- Progress bars per tier
- Click any card → expand **"What counts"** for the exact metric

---

## Core Mechanics

| Property | Detail |
|----------|--------|
| **Tiers** | Copper → Silver → Gold → Diamond → Olympian |
| **States** | **Unlocked** — earned at least one tier; **Discovered** — progress shown but not unlocked; **Secret** — hidden until triggered |
| **Scanning** | Analyzes `~/.hermes/state.db` (session history). First scan is incremental; later rescans are cached for speed. |
| **Progress Storage** | Saves to `state.json` |
| **Origin** | Originally community-made (`PCinkusz/hermes-achievements`), now bundled |
| **Kinds** | `best_session` (peak in one session), `lifetime` (cumulative), `multi_condition` (multiple metrics required) |

---

## Achievement Categories & Full Catalog

### 1. Agent Autonomy
> Focuses on letting the agent run independently. Great for training autonomous workflows.

| Achievement | Description | Tier Thresholds |
|-------------|-------------|-----------------|
| **Let Him Cook** | Max tool calls in one session | 200 / 500 / 1,200 / 3,000 / 8,000 |
| **Autonomous Avalanche** | Lifetime total tool calls | 1k / 3k / 8k / 20k / 50k |
| **Toolchain Maxxer** | Distinct tools in one session | 18 / 28 / 45 / 70 / 100 |
| **Full Send** | Multi-tool involvement (terminal + files + web/browser) | *(progressive thresholds)* |
| **Subagent Commander** | `delegate_task` calls | 5 / 40 / 100 / 1k / 5k |
| **Background Process Enjoyer** | Background process calls | 300 / 800 / 2k / 6k / 15k |
| **Cron Necromancer** | Cron / scheduled jobs | 1k / 3k / 8k / 20k / 50k |

---

### 2. Debugging Chaos
> Teaches debugging patterns and recovery — key for robust agent training.

| Achievement | Description | Tier Thresholds |
|-------------|-------------|-----------------|
| **Red Text Connoisseur** | Total errors encountered | 1.5k / 4k / 10k / 25k / 75k |
| **Stack Trace Sommelier** | Tracebacks encountered | 300 / 1k / 3k / 8k / 20k |
| **Actually Read The Logs** | Log reads | 1k / 3k / 8k / 20k / 50k |
| **Port 3000 Is Taken** *(secret)* | Port conflicts | 15 / 40 / 100 / 300 / 1k |
| **Permission Denied Any%** *(secret)* | Permission errors | 25 / 75 / 200 / 600 / 1.5k |
| **Dependency Hell Tourist** | Dependency-related issues | *(progressive thresholds)* |

---

### 3. Skills & Memory

| Achievement | Description |
|-------------|-------------|
| **Skillsmith** | Skill creation and usage |
| **Memory Keeper** | Memory writes/reads |
| **Context Dragon** | Long context sessions |
| **Plugin Goblin** | Plugin discovery/usage |

---

### 4. Model & Provider Variety

| Achievement | Description |
|-------------|-------------|
| **Provider Polyglot** | Using multiple model providers |
| **Two-Chain Mixer** | Chaining models/providers in one session |

---

### 5. Coding & Vibe-Coding

| Achievement | Description |
|-------------|-------------|
| **"This Was Supposed To Be Quick"** | Sessions that ran much longer than expected |
| **"One More Small Change"** | Repeated small edits/cycles |

---

### 6. Web Research & Browsing

| Achievement | Description |
|-------------|-------------|
| *(Web search / extraction milestones)* | Progressive thresholds for web tool usage |

---

### 7. Lifestyle Patterns

| Achievement | Description |
|-------------|-------------|
| *(Weekend warrior / night owl)* | Sessions during off-hours |

---

## How to Retrieve Reference Data (for Training & Education)

### Option A: Dashboard UI (Recommended)
```bash
hermes dashboard
# → Achievements tab → click any card → "What counts"
```

### Option B: Plugin API (Best for Data Export)
```bash
curl http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements
```

Returns full catalog as JSON including:
- ID, name, description, tiers, current progress, unlock timestamps
- Underlying counters/metrics

Other endpoints:
- `GET /scan-status` — scan progress
- `GET /recent-unlocks`
- `POST /rescan` — force fresh analysis
- `POST /reset-state` — reset progress

### Option C: Direct Files (Advanced)
```
~/.hermes/plugins/hermes-achievements/
├── state.json          # personal unlocks + timestamps
├── scan_snapshot.json  # cached full scan payload
└── scan_checkpoint.json # per-session stats cache
```

Source code: `plugin_api.py` in `PCinkusz/hermes-achievements` on GitHub.

---

## Educational Value

Hermes Achievements tracks **meta-behaviors** that are excellent for studying agent optimization:

| Meta-Behavior | What It Teaches |
|---------------|-----------------|
| Tool chaining | How to compose multi-step workflows |
| Debugging resilience | Error recovery patterns |
| Skill/memory leverage | When to persist vs. re-derive |
| Multi-provider use | Cost/performance trade-offs |
| Long context handling | Context window management |
| Background work | Autonomous agent patterns |

---

## Tips for Power Users

- **Rescan manually** after heavy sessions: `POST /rescan`
- **Export JSON** and analyze what behaviors unlock high-tier badges
- **Track progress programmatically** — script against the API to log your journey
- **New achievements** appear with Hermes updates; rescanning pulls the latest catalog
- **Secret achievements** are hidden until your history triggers the first signal — explore different workflows to discover them

---

## Related Resources

| Resource | URL |
|----------|-----|
| Hermes Agent Docs | https://hermes-agent.nousresearch.com |
| Achievements Plugin Source | https://github.com/PCinkusz/hermes-achievements |
| Community Discussions | https://reddit.com/r/hermesagent |

---

*Generated from live X/Grok conversation data and cross-referenced with official sources.*
