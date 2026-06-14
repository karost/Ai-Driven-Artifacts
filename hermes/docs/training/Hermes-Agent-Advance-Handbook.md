# Hermes Agent Advance Handbook — Achievement Mastery

> **Scope:** The complete Hermes Achievements system — condensed from the 500-line deep reference manual into a single study handbook.  
> **Source:** [`docs/hermes-achievements-training.md`](../hermes-achievements-training.md) (517 lines, 25 KB)  
> **Format:** Handbook — not unit-based. Organized by category with exact thresholds, strategies, and quick commands.  
> **Hermes Version:** v0.15.1 — Bundled plugin (no separate install)  
> **Date:** June 2026

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [The 9 Categories — Full Catalog](#2-the-9-categories--full-catalog)
3. [Secret Achievements](#3-secret-achievements)
4. [Playstyle Strategies](#4-playstyle-strategies)
5. [API Quick Reference](#5-api-quick-reference)
6. [Training Exercises](#6-training-exercises)
7. [Mastery Roadmap](#7-mastery-roadmap)
8. [Advance Track Units](#8-advance-track-units)

---

## 1. System Architecture

### What It Is

Hermes Achievements is a **Steam-style gamification layer** built into the Hermes Dashboard. It scans your real local session history (`~/.hermes/state.db`) and awards 60+ collectible tiered badges across 9 behavioral categories.

**Why:** Motivation, meta-learning, benchmarking, community.  
**When:** After every session save and dashboard rescan.

### Tier Progression

```
Copper → Silver → Gold → Diamond → Olympian
  Easy   Moderate  Hard    Expert   Mastery
```

Every badge has 5 thresholds. Progress tracks cumulatively (`lifetime`) or by peak (`best_session`) or by multi-condition (`multi_condition`).

### Achievement States

| State | Icon | Meaning | Visibility |
|-------|------|---------|------------|
| **Unlocked** | 🏆 | Earned at least one tier | Always |
| **Discovered** | 🔍 | Known, progress visible | After first signal |
| **Secret** | ❓ | Hidden until triggered | Invisible |

### Scanning Engine

```
~/.hermes/state.db (SQLite session history)
         ↓
   First scan: incremental, background
         ↓
   Snapshot cache → fast warm loads (120s TTL)
         ↓
   Checkpoint reuse for unchanged sessions
         ↓
   state.json (persistent unlocks + timestamps)
```

**Performance:** First scan = background, non-blocking. Rescans = sub-second cached.

### Where Files Live

```
~/.hermes/plugins/hermes-achievements/
├── dashboard/
│   └── plugin_api.py          ← Flask routes, badge definitions
├── state.json                 ← YOUR progress (never overwritten on update)
├── scan_snapshot.json         ← Cached scan payload
└── scan_checkpoint.json       ← Per-session stats hash
```

**Critical:** `state.json` is your persistent unlock state. Git pulls, plugin updates, and Hermes upgrades **never** touch it. New versions only evaluate new badges against existing history.

---

## 2. The 9 Categories — Full Catalog

### 2.1 Usage Milestones (16 badges)
> Lifetime counters. These are the backbone of your Legend run.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|----|------|------|--------|--------|--------|------|---------|----------|
| `first_blood` | First Blood | `lifetime` | First session | 1 | — | — | — | — |
| `centurion` | Centurion | `lifetime` | Total sessions | 100 | 300 | 1K | 3K | 10K |
| `marathon_runner` | Marathon Runner | `best_session` | Longest session (min) | 60 | 180 | 480 | 1,200 | 3,000 |
| `tool_century` | Tool Century | `lifetime` | Total tool calls | 10K | 30K | 100K | 300K | 1M |
| `file_master` | File Master | `lifetime` | File operations | 5K | 15K | 50K | 150K | 500K |
| `code_executor` | Code Executor | `lifetime` | `execute_code` runs | 1K | 3K | 10K | 30K | 100K |
| `terminal_tyrant` | Terminal Tyrant | `lifetime` | Terminal commands | 2K | 6K | 20K | 60K | 200K |
| `web_wanderer` | Web Wanderer | `lifetime` | Web search/extract | 5K | 15K | 50K | 150K | 500K |
| `vision_seeker` | Vision Seeker | `lifetime` | Vision/image analysis | 100 | 300 | 1K | 3K | 10K |
| `tts_bard` | TTS Bard | `lifetime` | Text-to-speech | 50 | 150 | 500 | 1,500 | 5K |
| `image_gen_artisan` | Image Gen Artisan | `lifetime` | Image generations | 50 | 150 | 500 | 1,500 | 5K |
| `compression_survivor` | Compression Survivor | `lifetime` | Context compressions | 10 | 30 | 100 | 300 | 1K |
| `checkpoint_champion` | Checkpoint Champion | `lifetime` | Checkpoints created | 50 | 150 | 500 | 1,500 | 5K |
| `memory_packer` | Memory Packer | `lifetime` | Memory consolidations | 10 | 30 | 100 | 300 | 1K |
| `curator_caller` | Curator Caller | `lifetime` | Curator invocations | 5 | 15 | 50 | 150 | 500 |
| `legend` | Legend | `multi_condition` | ALL metrics at Olympian | — | — | — | — | — |

**Key insight:** `tool_century` and `terminal_tyrant` will unlock naturally with daily use. `legend` requires reaching Olympian in every other category — the ultimate endgame.

---

### 2.2 Tool Proficiency (17 badges)
> Tool usage, autonomy, and the debugging that comes with it.

**Autonomy sub-group (7):**

| ID | Name | Kind | Metric | C | S | G | D | O |
|----|------|------|--------|---|---|---|---|---|
| `let_him_cook` | Let Him Cook | `best_session` | Max tool calls in one session | 200 | 500 | 1,200 | 3,000 | 8,000 |
| `autonomous_avalanche` | Autonomous Avalanche | `lifetime` | Total tool calls | 1K | 3K | 8K | 20K | 50K |
| `toolchain_maxxer` | Toolchain Maxxer | `best_session` | Max distinct tools in one session | 18 | 28 | 45 | 70 | 100 |
| `full_send` | Full Send | `multi_condition` | Terminal≥180 + File≥120 + Web≥60 | — | — | — | — | — |
| `subagent_commander` | Subagent Commander | `lifetime` | `delegate_task` calls | 5 | 40 | 100 | 1K | 5K |
| `background_process_enjoyer` | Background Process Enjoyer | `lifetime` | Background process calls | 300 | 800 | 2K | 6K | 15K |
| `cron_necromancer` | Cron Necromancer | `lifetime` | Cron/scheduled jobs | 1K | 3K | 8K | 20K | 50K |

**Debugging sub-group (10):**

| ID | Name | Kind | Metric | C | S | G | D | O | Secret |
|----|------|------|--------|---|---|---|---|---|--------|
| `red_text_connoisseur` | Red Text Connoisseur | `lifetime` | Total errors | 1.5K | 4K | 10K | 25K | 75K | |
| `stack_trace_sommelier` | Stack Trace Sommelier | `lifetime` | Traceback events | 300 | 1K | 3K | 8K | 20K | |
| `actually_read_the_logs` | Actually Read The Logs | `lifetime` | Log reads | 1K | 3K | 8K | 20K | 50K | |
| `port_3000_taken` | Port 3000 Is Taken | `lifetime` | Port conflicts | 15 | 40 | 100 | 300 | 1K | ✅ |
| `permission_denied_any_percent` | Permission Denied Any% | `lifetime` | Permission errors | 25 | 75 | 200 | 600 | 1.5K | ✅ |
| `dependency_hell_tourist` | Dependency Hell Tourist | `multi_condition` | Install errors≥25 + successes≥10 | — | — | — | — | — | |
| `the_fix_was_restarting` | The Fix Was Restarting | `multi_condition` | Restart-after-error≥50 + total errors≥4K | — | — | — | — | — | |
| `forgot_the_env_var` | Forgot The Env Var | `lifetime` | Env var errors | 5K | 15K | 40K | 100K | 250K | ✅ |
| `yaml_colon_incident` | YAML Colon Incident | `lifetime` | YAML errors | 1K | 3K | 8K | 20K | 50K | ✅ |
| `docker_name_collision` | Docker Name Collision | `lifetime` | Docker conflicts | 75 | 200 | 600 | 1.5K | 4K | ✅ |

**Strategy:** `subagent_commander` + `background_process_enjoyer` unlock together. `let_him_cook` requires one massive session — use `delegate_task` for parallelism on a 2015 MBP with thermal throttling.

---

### 2.3 Model Diversity (5 badges)
> New in v0.2.x. Celebrates model/provider exploration.

| ID | Name | Kind | Metric | C | S | G | D | O |
|----|------|------|--------|---|---|---|---|---|
| `five_model_flight` | Five-Model Flight | `best_session` | 5+ models in one session | — | — | — | — | — |
| `provider_polyglot` | Provider Polyglot | `lifetime` | Distinct providers used | 3 | 5 | 8 | 12 | 18 |
| `claude_confidant` | Claude Confidant | `lifetime` | Claude-specific sessions | 50 | 150 | 400 | 1K | 3K |
| `gemini_cartographer` | Gemini Cartographer | `lifetime` | Gemini-specific sessions | 50 | 150 | 400 | 1K | 3K |
| `open_weights_pilgrim` | Open Weights Pilgrim | `lifetime` | Local/OSS model sessions | 50 | 150 | 400 | 1K | 3K |

**Strategy:** Use `/model` to switch providers mid-session for `five_model_flight`. `provider_polyglot` requires trying Ollama Cloud (Kimi-K2.6, GLM-5.1, Qwen), Anthropic, OpenRouter, and local models.

---

### 2.4 Memory & Research (7 badges)

| ID | Name | Kind | Metric | C | S | G | D | O |
|----|------|------|--------|---|---|---|---|---|
| `rabbit_hole_certified` | Rabbit Hole Certified | `lifetime` | Total web calls | 400 | 1.2K | 3K | 8K | 20K |
| `citation_goblin` | Citation Goblin | `lifetime` | `web_extract` calls | 100 | 300 | 1K | 3K | 8K |
| `docs_archaeologist` | Docs Archaeologist | `lifetime` | Documentation reads | 200 | 600 | 1.5K | 4K | 10K |
| `search_orchestrator` | Search Orchestrator | `best_session` | Max web calls in one session | 50 | 150 | 400 | 1K | 3K |
| `memory_keeper` | Memory Keeper | `lifetime` | Memory events | 100 | 300 | 1K | 3K | 8K |
| `memory_palace` | Memory Palace | `lifetime` | Memory write events | 100 | 300 | 1K | 3K | 8K |
| `context_dragon` | Context Dragon | `lifetime` | Context events | 5K | 15K | 40K | 100K | 250K |

**Strategy:** `rabbit_hole_certified` is the signature research badge. Combine `web_search` + `web_extract` + `browser` for deep dives. `memory_keeper` + `memory_palace` unlock together with regular `memory` tool use.

---

### 2.5 Skills & Automation (8 badges)

| ID | Name | Kind | Metric | C | S | G | D | O |
|----|------|------|--------|---|---|---|---|---|
| `skillsmith` | Skillsmith | `lifetime` | Skill events | 5K | 15K | 40K | 100K | 250K |
| `skill_issue_skill_created` | Skill Issue? Skill Created. | `lifetime` | `skill_manage` events | 25 | 75 | 200 | 600 | 1.5K |
| `gateway_dweller` | Gateway Dweller | `lifetime` | Gateway events | 5K | 15K | 40K | 100K | 250K |
| `plugin_goblin` | Plugin Goblin | `lifetime` | Plugin events | 1K | 3K | 8K | 20K | 50K |
| `rollback_wizard` | Rollback Wizard | `lifetime` | Rollback events | 500 | 1.5K | 4K | 10K | 25K | ✅ |

*Note:* `memory_keeper`, `memory_palace`, `context_dragon`, `subagent_commander`, `cron_necromancer`, `background_process_enjoyer` badges also appear in Skills & Automation tracking context (overlap is intentional — achievements are not mutually exclusive by category).

**Strategy:** `skillsmith` is the highest-tier native badge. Use `skill_manage` frequently. Gateway Dweller requires running the messaging gateway (Telegram, Discord, etc.).

---

### 2.6 Session Quality (7 badges)

| ID | Name | Kind | Metric | C | S | G | D | O |
|----|------|------|--------|---|---|---|---|---|
| `supposed_to_be_quick` | This Was Supposed To Be Quick | `best_session` | Max messages in one session | 300 | 600 | 1.2K | 2.5K | 6K |
| `one_more_small_change` | One More Small Change | `best_session` | Max file tool calls in one session | 150 | 400 | 1K | 3K | 8K |
| `vibe_architect` | Vibe Architect | `best_session` | Max files touched in one session | 300 | 700 | 1.5K | 4K | 10K |
| `weekend_warrior` | Weekend Warrior | `lifetime` | Weekend sessions | 10 | 30 | 80 | 200 | 500 |
| `night_owl` | Night Owl | `lifetime` | Night sessions (22:00–05:00) | 20 | 60 | 150 | 400 | 1K |
| `early_bird_cron` | Early Bird Cron | `lifetime` | Morning cron jobs (05:00–09:00) | 5 | 15 | 40 | 100 | 250 |
| `marathon_runner` | Marathon Runner | `best_session` | Longest session (min) | 60 | 180 | 480 | 1.2K | 3K |

**Strategy:** Lifestyle badges are **time-gated** — cannot be rushed. Vibe Coding badges unlock during long debugging/refactoring sessions intentionally.

---

### 2.7 Social & Community (3 badges)

| ID | Name | Kind | Metric | C | S | G | D | O |
|----|------|------|--------|---|---|---|---|---|
| `shared_session` | Shared Session | `lifetime` | Sessions shared/exported | 5 | 15 | 40 | 100 | 250 |
| `team_delegate` | Team Delegate | `lifetime` | Multi-user delegate calls | 10 | 30 | 80 | 200 | 500 |
| `cross_platform` | Cross Platform | `lifetime` | Platforms used (CLI + Gateway) | 2 | 3 | 4 | 5 | 6 |

**Strategy:** `cross_platform` is the easiest — just connect CLI **and** Telegram gateway. `shared_session` requires exporting trajectories to agentskills.io.

---

### 2.8 Secret Achievements (8 badges)
> Invisible until your first triggering session. See §3 for unlock hints.

| Badge | Unlock Trigger |
|-------|---------------|
| Port 3000 Is Taken | Server processes hit port conflicts |
| Permission Denied Any% | Sudo/chmod/Docker permission failures |
| Forgot The Env Var | Config loading with missing env vars |
| YAML Colon Incident | YAML edits with syntax errors |
| Docker Name Collision | Duplicate container names |
| Rollback Wizard | Frequent `/rollback` after mistakes |
| One Character Fix | Fix a bug with a 1-character patch |
| Legend | Reach Olympian in ALL other badges |

**Strategy:** Most secret badges unlock **accidentally** during normal workflows. Only `legend` requires grind. `rollback_wizard` is actively farmable.

---

## 3. Secret Achievements (Detailed)

### 3.1 How Secret Detection Works

The scanning engine classifies achievements by **regex match** on session tool output:

```python
# Conceptual classifier (from plugin_api.py)
HINT_PATTERNS = {
    "port_3000_taken": r"Address already in use.*:3000",
    "permission_denied_any_percent": r"Permission denied|EACCES",
    "forgot_the_env_var": r"KeyError.*env|Environment variable",
    "yaml_colon_incident": r"yaml\.(scanner|parser|constructor)",
    "docker_name_collision": r"container name.*already in use",
    "rollback_wizard": r"/rollback.* executed",
    "one_character_fix": r"single character|one char fix",
}
```

When a pattern matches for the first time:
1. Badge flips from **Secret** (invisible) → **Discovered** (visible, progress=0)
2. All previous session history is re-scanned for additional matches
3. Progress updates to `lifetime count` of matches

### 3.2 Legend — The Ultimate Badge

**Requirement:** Reach Olympian tier in **ALL** other 59 badges.

**Why it's the endgame:** No single strategy works. You need:
- Vibe-coding marathons (`supposed_to_be_quick` + `one_more_small_change` + `vibe_architect`)
- Daily tool grinding (`tool_century`, `terminal_tyrant`, `web_wanderer`)
- Provider polyglot (`provider_polyglot` at 18 providers)
- All model-specific badges at Olympian
- All secret badges maxed out
- All lifestyle badges at Olympian (time-gated — this takes months)

**Verification:**
```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '[.achievements[] | select(.tier == "olympian")] | length'
# When this returns 59 or more, Legend is the only badge remaining.
```

---

## 4. Playstyle Strategies

### 🚀 Speedrunner — 10 badges in 1 week

| Priority | Badge | How |
|----------|-------|-----|
| 1 | First Blood | Complete your first session |
| 2 | Red Text Connoisseur | Use Hermes normally — errors happen |
| 3 | Actually Read The Logs | Check logs with `/logs` or `read_file` |
| 4 | Memory Keeper | Use `memory` tool frequently |
| 5 | Rabbit Hole Certified | Research topics with `web_search` |
| 6 | Toolchain Maxxer | Use 18+ different tools in one session |
| 7 | Weekend Warrior | Use Hermes on Saturday/Sunday |
| 8 | File Master | Edit files with `write_file` / `patch` |
| 9 | Code Executor | Run Python with `execute_code` |
| 10 | Terminal Tyrant | Execute shell commands |

### 🏗️ Architect — Maximize Native + Vibe Coding

| Priority | Badge | Strategy |
|----------|-------|----------|
| 1 | This Was Supposed To Be Quick | Start a refactor, let it spiral |
| 2 | One More Small Change | Iterate on one file 150+ times |
| 3 | Vibe Architect | Touch 300+ files in one session |
| 4 | Ship First, Ask Later | Git commit + push from Hermes |
| 5 | CSS Exorcist | Frontend projects with styling |
| 6 | Skillsmith | Create skills from coding patterns |
| 7 | Memory Palace | Write memory entries after each session |
| 8 | Context Dragon | Long context sessions with compression |

### 🔬 Researcher — Information Forager

| Priority | Badge | Strategy |
|----------|-------|----------|
| 1 | Rabbit Hole Certified | Deep-dive with 20+ web calls |
| 2 | Citation Goblin | `web_extract` on every source |
| 3 | Docs Archaeologist | Read documentation files |
| 4 | Search Orchestrator | 50+ web calls in one session |
| 5 | Provider Polyglot | Switch models with `/model` |
| 6 | Claude Confidant | Use Anthropic Claude exclusively |
| 7 | Five-Model Flight | Use 5 models in one long session |
| 8 | Open Weights Pilgrim | Run local models via Ollama |

### 🤖 Autonomy Engineer — Background Work

| Priority | Badge | Strategy |
|----------|-------|----------|
| 1 | Let Him Cook | One session with 200+ tool calls |
| 2 | Subagent Commander | Spawn 5+ `delegate_task` children |
| 3 | Background Process Enjoyer | Run `terminal(background=True)` |
| 4 | Cron Necromancer | Schedule jobs with `cronjob` tool |
| 5 | Full Send | Heavy terminal + file + web in one session |
| 6 | Autonomous Avalanche | Just keep using Hermes daily |

### 🎯 Secret Hunter

| Secret | Action |
|--------|--------|
| Port 3000 Is Taken | Start a server, then try again |
| Permission Denied Any% | Run `sudo` commands that fail |
| Forgot The Env Var | Load configs with missing env vars |
| YAML Colon Incident | Edit YAML with syntax errors |
| Docker Name Collision | `docker run --name same` twice |
| Rollback Wizard | Use `/rollback` after bad edits |
| One Character Fix | Fix a bug with a 1-char patch |
| Legend | Olympian everywhere |

---

## 5. API Quick Reference

### Dashboard Endpoints

```
Base: http://127.0.0.1:9119/api/plugins/hermes-achievements/
```

| Method | Endpoint | Returns |
|--------|----------|---------|
| GET | `/achievements` | Full catalog + your progress |
| GET | `/scan-status` | Current scan state |
| GET | `/recent-unlocks` | Recently earned badges |
| GET | `/sessions/{id}/badges` | Badges for a specific session |
| POST | `/rescan` | Force full rescan |
| POST | `/reset-state` | Wipe all progress (irreversible!) |

### Useful Commands

```bash
# Export all progress to JSON
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | {name, tier, progress, unlocked}' > my_progress.json

# Check recent unlocks
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/recent-unlocks \
  | jq '.[] | {name, tier, unlocked_at}'

# Count Olympian badges
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '[.achievements[] | select(.tier == "olympian")] | length'

# Force rescan (safe — never wipes progress)
curl -X POST http://127.0.0.1:9119/api/plugins/hermes-achievements/rescan

# Reset state (DANGEROUS — wipes all progress)
curl -X POST http://127.0.0.1:9119/api/plugins/hermes-achievements/reset-state
```

### State Files

```
~/.hermes/plugins/hermes-achievements/
├── state.json              # Persistent unlocks + timestamps
├── scan_snapshot.json      # Cached scan payload (120s TTL)
└── scan_checkpoint.json    # Per-session stats cache
```

---

## 6. Training Exercises

### Exercise 1: First Blood + Toolchain Maxxer (30 min)
**Goal:** Unlock 2 badges in one session.

1. Start Hermes: `hermes --tui`
2. Use at least 18 different tools:
   - `web_search`, `web_extract`, `read_file`, `write_file`, `terminal`, `execute_code`, `browser_navigate`, `memory`, `skill_manage`, `delegate_task`, `cronjob`, `todo`, `clarify`, `session_search`, `fact_store`, `image_generate`, `tts`, `vision_analyze`
3. Type `/save` and exit
4. Run: `hermes dashboard` → Achievements tab → verify

### Exercise 2: Vibe Coding Gauntlet (2 hours)
**Goal:** Unlock 3 Vibe Coding badges.

1. Pick a small project (Python script or HTML page)
2. Iterate 150+ times on one file
3. Touch 300+ files (create temp files if needed)
4. Let session run 300+ messages
5. Check dashboard for: This Was Supposed To Be Quick, One More Small Change, Vibe Architect

### Exercise 3: Research Rabbit Hole (1 hour)
**Goal:** Unlock Rabbit Hole Certified + Citation Goblin.

1. Pick a complex topic (e.g., Qdrant optimization)
2. Use `web_search` 20+ times
3. Use `web_extract` on 10+ sources
4. Use `browser_navigate` for documentation
5. Create summary with `write_file`

### Exercise 4: Secret Hunter
**Goal:** Discover all 8 secret achievements.

See §4 Playstyle Strategy → Secret Hunter table.

---

## 7. Mastery Roadmap

| Phase | Time | Target | Key Badges |
|-------|------|--------|-----------|
| **Beginner** | Week 1–2 | 15+ badges, mostly Copper/Silver | First Blood, Centurion, Red Text Connoisseur, Actually Read The Logs, Memory Keeper, Rabbit Hole Certified, Toolchain Maxxer, Weekend Warrior, Night Owl |
| **Intermediate** | Week 3–6 | 30+ badges, Gold on favorites | All Vibe Coding, Skillsmith, Subagent Commander, Provider Polyglot, File Master, Code Executor, Terminal Tyrant |
| **Advanced** | Month 2–3 | 45+ badges, Diamond on core | Cron Necromancer, Full Send, Autonomous Avalanche, Tool Century, Context Dragon, Marathon Runner, Pixel Goblin, CSS Exorcist |
| **Master** | Month 4–6 | 55+ badges, Olympian on 10+ | All Model/Provider at Olympian, all Lifestyle at Olympian, all Secrets discovered, Compression Survivor, Checkpoint Champion, Curator Caller |
| **Legend** | Month 6+ | Legend badge | Olympian in ALL 59 other badges |

---

## 8. Advance Track Units

For **hands-on step-by-step labs** with annotated source code and the full 23-point pedagogical structure, see the Advance Track:

| Unit | Category | File |
|------|----------|------|
| 01 | Usage Milestones | [Unit_01.md](Units-Advance/Unit_01.md) |
| 02 | Tool Proficiency | [Unit_02.md](Units-Advance/Unit_02.md) |
| 03 | Model Diversity | [Unit_03.md](Units-Advance/Unit_03.md) |
| 04 | Memory & Research | [Unit_04.md](Units-Advance/Unit_04.md) |
| 05 | Skills & Automation | [Unit_05.md](Units-Advance/Unit_05.md) |
| 06 | Error & Recovery | [Unit_06.md](Units-Advance/Unit_06.md) |
| 07 | Session Quality | [Unit_07.md](Units-Advance/Unit_07.md) |
| 08 | Social & Community | [Unit_08.md](Units-Advance/Unit_08.md) |
| 09 | Secret Achievements | [Unit_09.md](Units-Advance/Unit_09.md) |

Each unit contains:
- **Lab** (operator hands-on with exact commands)
- **Chapter** (architect analysis with source code)
- **Master Prompt** (ready-to-copy for Kimi-K2.6)
- **5 Questions** (active recall)

---

## Appendix: Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                 HERMES ACHIEVEMENTS CHEAT SHEET             │
├─────────────────────────────────────────────────────────────┤
│  9 Categories    │ 60 Badges    │ 5 Tiers                    │
│  8 Secrets       │ 3 Kinds      │ Copper→Silver→Gold→D→O   │
├─────────────────────────────────────────────────────────────┤
│  MILESTONES  │ 16 │ AUTONOMY   │ 7  │ VIBE CODING  │ 7    │
│  MODEL LORE   │ 5  │ RESEARCH   │ 7  │ SKILLS       │ 8    │
│  LIFESTYLE    │ 3  │ SOCIAL     │ 3  │              │      │
├─────────────────────────────────────────────────────────────┤
│  Dashboard: hermes dashboard → Achievements                   │
│  API: curl localhost:9119/api/plugins/hermes-achievements/   │
│  Rescan: POST /rescan                                       │
│  Share: PNG cards (1200×630) on unlocked badges             │
└─────────────────────────────────────────────────────────────┘
```

---

*Last updated: June 2026 — Hermes v0.15.1. Badge data sourced from live `hermes-achievements-training.md` and GitHub repo `PCinkusz/hermes-achievements`.*
