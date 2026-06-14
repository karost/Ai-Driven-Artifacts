# Hermes Achievements — Deep Training Manual

> **Purpose:** Comprehensive training material for mastering the Hermes Agent achievements system.  
> **Sources:** Grok conversation research, official Hermes docs, `PCinkusz/hermes-achievements` GitHub repo, raw `plugin_api.py` source code, Nous Research bundled plugin docs, community Reddit discussions.  
> **Coverage:** All ~60 achievements across 9 categories with exact tier thresholds, secret flags, and unlock strategies.  
> **Last updated:** June 2026

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Core Mechanics Deep-Dive](#2-core-mechanics-deep-dive)
3. [Complete Achievement Catalog (60 Badges)](#3-complete-achievement-catalog)
4. [Secret Achievements](#4-secret-achievements)
5. [Unlock Strategies by Playstyle](#5-unlock-strategies-by-playstyle)
6. [API Reference for Programmatic Tracking](#6-api-reference)
7. [Training Exercises](#7-training-exercises)
8. [Achievement Mastery Roadmap](#8-achievement-mastery-roadmap)

---

## 1. System Overview

Hermes Achievements is a **Steam-style gamification layer** built into the Hermes Dashboard. It transforms your agent usage into a collectible badge system with 60+ tiered achievements across 9 behavioral categories.

### Why It Exists
- **Motivation:** Makes agent workflows feel like discovering Easter eggs
- **Meta-learning:** Surfaces usage patterns you didn't know you had
- **Benchmarking:** Quantifies your Hermes proficiency across dimensions
- **Community:** Share progress (PNG share cards added in v0.4.0, May 2026)

### Origin Story
| Phase | Detail |
|-------|--------|
| **v0.1.x** | Community plugin by [@PCinkusz](https://github.com/PCinkusz) |
| **v0.2.x** | Expanded to 60+ badges including model/provider achievements |
| **v0.3.0** | Scan performance refactored (snapshot cache + incremental checkpoint) |
| **v0.4.0** | Share cards (1200×630 PNG) for social media |
| **Bundled** | Now ships with Hermes Agent core — no separate install needed |

---

## 2. Core Mechanics Deep-Dive

### 2.1 Tier Progression Ladder

```
Copper → Silver → Gold → Diamond → Olympian
   ↑        ↑        ↑         ↑         ↑
  Easy   Moderate  Hard    Expert   Mastery
```

Each achievement has **5 thresholds**. Progress is tracked cumulatively (`lifetime`) or by peak performance (`best_session`).

### 2.2 Achievement Kinds

| Kind | How It Tracks | Example |
|------|---------------|---------|
| `best_session` | Peak value in a single session | Most tool calls in one chat |
| `lifetime` | Cumulative across all history | Total errors encountered |
| `multi_condition` | Multiple metrics must satisfy | Terminal + file + web usage together |

### 2.3 States

| State | Icon | Meaning | Visibility |
|-------|------|---------|------------|
| **Unlocked** | 🏆 | Earned at least one tier | Always visible |
| **Discovered** | 🔍 | Known but not earned | Visible with progress bar |
| **Secret** | ❓ | Hidden until first trigger | Invisible until triggered |

### 2.4 Scanning Engine

```
~/.hermes/state.db (session history)
         ↓
   First scan: incremental (background)
         ↓
   Snapshot cache → fast warm loads
         ↓
   Checkpoint reuse for unchanged sessions
         ↓
   state.json (your personal progress)
```

**Performance facts:**
- First scan: background, non-blocking
- Rescans: cached, sub-second
- `SNAPSHOT_TTL_SECONDS = 120`

---

## 3. Complete Achievement Catalog

### 3.1 Agent Autonomy (7 achievements)
> Let the agent run independently. Great for autonomous workflows.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|----|------|------|--------|--------|--------|------|---------|----------|
| `let_him_cook` | Let Him Cook | `best_session` | Max tool calls in one session | 200 | 500 | 1,200 | 3,000 | 8,000 |
| `autonomous_avalanche` | Autonomous Avalanche | `lifetime` | Total tool calls | 1k | 3k | 8k | 20k | 50k |
| `toolchain_maxxer` | Toolchain Maxxer | `best_session` | Max distinct tools in one session | 18 | 28 | 45 | 70 | 100 |
| `full_send` | Full Send | `multi_condition` | Terminal≥180 + File≥120 + Web/Browser≥60 | — | — | — | — | — |
| `subagent_commander` | Subagent Commander | `lifetime` | `delegate_task` calls | 5 | 40 | 100 | 1,000 | 5,000 |
| `background_process_enjoyer` | Background Process Enjoyer | `lifetime` | Background process calls | 300 | 800 | 2,000 | 6,000 | 15,000 |
| `cron_necromancer` | Cron Necromancer | `lifetime` | Cron/scheduled job calls | 1k | 3k | 8k | 20k | 50k |

**Training tip:** Run `delegate_task` for parallel subagents and background processes to unlock both Subagent Commander and Background Process Enjoyer simultaneously.

---

### 3.2 Debugging Chaos (10 achievements)
> Embrace errors. These teach debugging patterns and recovery — key for robust agents.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian | 🔒 |
|----|------|------|--------|--------|--------|------|---------|----------|----|
| `red_text_connoisseur` | Red Text Connoisseur | `lifetime` | Total errors | 1.5k | 4k | 10k | 25k | 75k | |
| `stack_trace_sommelier` | Stack Trace Sommelier | `lifetime` | Traceback events | 300 | 1k | 3k | 8k | 20k | |
| `actually_read_the_logs` | Actually Read The Logs | `lifetime` | Log read events | 1k | 3k | 8k | 20k | 50k | |
| `port_3000_taken` | Port 3000 Is Taken | `lifetime` | Port conflicts | 15 | 40 | 100 | 300 | 1,000 | ✅ |
| `permission_denied_any_percent` | Permission Denied Any% | `lifetime` | Permission denied events | 25 | 75 | 200 | 600 | 1,500 | ✅ |
| `dependency_hell_tourist` | Dependency Hell Tourist | `multi_condition` | Install errors≥25 + successes≥10 | — | — | — | — | — | |
| `the_fix_was_restarting` | The Fix Was Restarting It | `multi_condition` | Restart-after-error≥50 + total errors≥4000 | — | — | — | — | — | |
| `forgot_the_env_var` | Forgot The Env Var | `lifetime` | Env var errors | 5k | 15k | 40k | 100k | 250k | ✅ |
| `yaml_colon_incident` | YAML Colon Incident | `lifetime` | YAML errors | 1k | 3k | 8k | 20k | 50k | ✅ |
| `docker_name_collision` | Docker Name Collision | `lifetime` | Docker conflict events | 75 | 200 | 600 | 1,500 | 4,000 | ✅ |

**Training tip:** Red Text Connoisseur is the easiest to unlock naturally — just use Hermes regularly. Permission Denied Any% and Port 3000 Is Taken require running server-related tools or Docker workflows.

---

### 3.3 Vibe Coding (7 achievements)
> For the flow-state coders. Tracks file edits, frontend work, and "just one more change" sessions.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian | 🔒 |
|----|------|------|--------|--------|--------|------|---------|----------|----|
| `supposed_to_be_quick` | This Was Supposed To Be Quick | `best_session` | Max messages in one session | 300 | 600 | 1,200 | 2,500 | 6,000 | |
| `one_more_small_change` | One More Small Change | `best_session` | Max file tool calls in one session | 150 | 400 | 1,000 | 3,000 | 8,000 | |
| `vibe_architect` | Vibe Architect | `best_session` | Max files touched in one session | 300 | 700 | 1,500 | 4,000 | 10,000 | |
| `pixel_goblin` | Pixel Goblin | `lifetime` | Frontend activity events | 20k | 50k | 120k | 300k | 800k | |
| `ship_first_ask_later` | Ship First, Ask Later | `multi_condition` | Git events≥50 + max tool calls≥500 | — | — | — | — | — | |
| `css_exorcist` | CSS Exorcist | `lifetime` | CSS activity events | 10k | 30k | 80k | 200k | 500k | |
| `one_character_fix` | One Character Fix | `multi_condition` | Tiny patch after errors≥5 + total errors≥4000 | — | — | — | — | — | ✅ |

**Training tip:** "This Was Supposed To Be Quick" unlocks during long debugging or refactoring sessions. "One More Small Change" is the classic vibe-coding badge — iterate on a file repeatedly.

---

### 3.4 Hermes Native (8 achievements)
> Master Hermes's own systems: skills, memory, context, gateway, plugins.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian | 🔒 |
|----|------|------|--------|--------|--------|------|---------|----------|----|
| `skillsmith` | Skillsmith | `lifetime` | Skill events | 5k | 15k | 40k | 100k | 250k | |
| `skill_issue_skill_created` | Skill Issue? Skill Created. | `lifetime` | `skill_manage` events | 25 | 75 | 200 | 600 | 1,500 | |
| `memory_keeper` | Memory Keeper | `lifetime` | Memory events | 100 | 300 | 1,000 | 3,000 | 8,000 | |
| `memory_palace` | Memory Palace | `lifetime` | Memory write events | 100 | 300 | 1,000 | 3,000 | 8,000 | |
| `context_dragon` | Context Dragon | `lifetime` | Context events | 5k | 15k | 40k | 100k | 250k | |
| `gateway_dweller` | Gateway Dweller | `lifetime` | Gateway events | 5k | 15k | 40k | 100k | 250k | |
| `plugin_goblin` | Plugin Goblin | `lifetime` | Plugin events | 1k | 3k | 8k | 20k | 50k | |
| `rollback_wizard` | Rollback Wizard | `lifetime` | Rollback events | 500 | 1,500 | 4,000 | 10,000 | 25,000 | ✅ |

**Training tip:** Skillsmith is the highest-tier native badge. Use `memory` and `skill_manage` tools frequently. Gateway Dweller requires running the messaging gateway (Telegram, Discord, etc.).

---

### 3.5 Research / Web (4 achievements)
> For the information foragers. Tracks web search, extraction, and documentation diving.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|----|------|------|--------|--------|--------|------|---------|----------|
| `rabbit_hole_certified` | Rabbit Hole Certified | `lifetime` | Total web calls | 400 | 1,200 | 3,000 | 8,000 | 20,000 |
| `citation_goblin` | Citation Goblin | `lifetime` | `web_extract` calls | 100 | 300 | 1,000 | 3,000 | 8,000 |
| `docs_archaeologist` | Docs Archaeologist | `lifetime` | Documentation reads | 200 | 600 | 1,500 | 4,000 | 10,000 |
| `search_orchestrator` | Search Orchestrator | `best_session` | Max web calls in one session | 50 | 150 | 400 | 1,000 | 3,000 |

**Training tip:** Rabbit Hole Certified is the signature research badge. Use `web_search` and `web_extract` aggressively on complex topics. Combine with `browser` tool for deep dives.

---

### 3.6 Model & Provider Lore (5 achievements)
> New in v0.2.x. Celebrate model diversity and provider exploration.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|----|------|------|--------|--------|--------|------|---------|----------|
| `five_model_flight` | Five-Model Flight | `best_session` | 5+ models used in one session | — | — | — | — | — |
| `provider_polyglot` | Provider Polyglot | `lifetime` | Distinct providers used | 3 | 5 | 8 | 12 | 18 |
| `claude_confidant` | Claude Confidant | `lifetime` | Claude-specific sessions | 50 | 150 | 400 | 1,000 | 3,000 |
| `gemini_cartographer` | Gemini Cartographer | `lifetime` | Gemini-specific sessions | 50 | 150 | 400 | 1,000 | 3,000 |
| `open_weights_pilgrim` | Open Weights Pilgrim | `lifetime` | Local/OSS model sessions | 50 | 150 | 400 | 1,000 | 3,000 |

**Training tip:** Use `/model` to switch providers mid-session for Five-Model Flight. Provider Polyglot requires trying Ollama Cloud (Kimi-K2.6, GLM-5.1, Qwen), Anthropic, OpenRouter, and local models.

---

### 3.7 Lifestyle Patterns (3 achievements)
> When you use Hermes matters as much as how.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|----|------|------|--------|--------|--------|------|---------|----------|
| `weekend_warrior` | Weekend Warrior | `lifetime` | Weekend sessions | 10 | 30 | 80 | 200 | 500 |
| `night_owl` | Night Owl | `lifetime` | Night sessions (22:00–05:00) | 20 | 60 | 150 | 400 | 1,000 |
| `early_bird_cron` | Early Bird Cron | `lifetime` | Morning cron jobs (05:00–09:00) | 5 | 15 | 40 | 100 | 250 |

**Training tip:** These are time-gated — you can't rush them. Weekend Warrior is the easiest lifestyle badge.

---

### 3.8 Social & Collaboration (3 achievements)
> Share, delegate, collaborate.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|----|------|------|--------|--------|--------|------|---------|----------|
| `shared_session` | Shared Session | `lifetime` | Sessions shared/exported | 5 | 15 | 40 | 100 | 250 |
| `team_delegate` | Team Delegate | `lifetime` | Multi-user delegate calls | 10 | 30 | 80 | 200 | 500 |
| `cross_platform` | Cross Platform | `lifetime` | Platforms used (CLI + Gateway) | 2 | 3 | 4 | 5 | 6 |

---

### 3.9 Milestones & Mastery (16 achievements)
> The big ones. Lifetime totals and rare feats.

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian | 🔒 |
|----|------|------|--------|--------|--------|------|---------|----------|----|
| `first_blood` | First Blood | `lifetime` | First session completed | 1 | — | — | — | — | |
| `centurion` | Centurion | `lifetime` | Total sessions | 100 | 300 | 1,000 | 3,000 | 10,000 | |
| `marathon_runner` | Marathon Runner | `best_session` | Longest session (minutes) | 60 | 180 | 480 | 1,200 | 3,000 | |
| `tool_century` | Tool Century | `lifetime` | Total tool calls | 10k | 30k | 100k | 300k | 1M | |
| `file_master` | File Master | `lifetime` | File operations | 5k | 15k | 50k | 150k | 500k | |
| `code_executor` | Code Executor | `lifetime` | `execute_code` runs | 1k | 3k | 10k | 30k | 100k | |
| `terminal_tyrant` | Terminal Tyrant | `lifetime` | Terminal commands | 2k | 6k | 20k | 60k | 200k | |
| `web_wanderer` | Web Wanderer | `lifetime` | Web search/extract | 5k | 15k | 50k | 150k | 500k | |
| `vision_seeker` | Vision Seeker | `lifetime` | Vision/image analysis | 100 | 300 | 1,000 | 3,000 | 10,000 | |
| `tts_bard` | TTS Bard | `lifetime` | Text-to-speech uses | 50 | 150 | 500 | 1,500 | 5,000 | |
| `image_gen_artisan` | Image Gen Artisan | `lifetime` | Image generations | 50 | 150 | 500 | 1,500 | 5,000 | |
| `compression_survivor` | Compression Survivor | `lifetime` | Context compressions | 10 | 30 | 100 | 300 | 1,000 | |
| `checkpoint_champion` | Checkpoint Champion | `lifetime` | Checkpoints created | 50 | 150 | 500 | 1,500 | 5,000 | |
| `memory_packer` | Memory Packer | `lifetime` | Memory consolidations | 10 | 30 | 100 | 300 | 1,000 | |
| `curator_caller` | Curator Caller | `lifetime` | Curator invocations | 5 | 15 | 50 | 150 | 500 | |
| `legend` | Legend | `multi_condition` | ALL metrics at Olympian | — | — | — | — | — | ✅ |

**Training tip:** Legend is the ultimate secret achievement — requires reaching Olympian tier in ALL other achievements. This is the true endgame.

---

## 4. Secret Achievements

Secret achievements are **invisible** until your session history triggers the first signal. Here are all 8 secrets with unlock hints:

| Secret Badge | Hint to Unlock |
|--------------|----------------|
| Port 3000 Is Taken | Run server processes (Docker, Node, Python) that hit port conflicts |
| Permission Denied Any% | Use `sudo`, `chmod`, or Docker commands that fail with permissions |
| Forgot The Env Var | Have many `.env` or config loading failures across sessions |
| YAML Colon Incident | Edit YAML files (configs, GitHub Actions) and trigger syntax errors |
| Docker Name Collision | Run Docker containers with duplicate names |
| Rollback Wizard | Use `/rollback` frequently after mistakes |
| One Character Fix | Make tiny single-character patches immediately after errors |
| Legend | Reach Olympian in ALL other achievements |

---

## 5. Unlock Strategies by Playstyle

### 🚀 Speedrunner (Fastest to First Unlock)
Target: Get 10+ badges in 1 week

| Priority | Badge | How |
|----------|-------|-----|
| 1 | First Blood | Complete your first session |
| 2 | Red Text Connoisseur | Use Hermes normally — errors happen |
| 3 | Actually Read The Logs | Check logs with `/logs` or `read_file` |
| 4 | Memory Keeper | Use `memory` tool frequently |
| 5 | Rabbit Hole Certified | Research topics with `web_search` |
| 6 | Toolchain Maxxer | In one session, use many different tools |
| 7 | Weekend Warrior | Use Hermes on Saturday/Sunday |
| 8 | File Master | Edit files with `write_file` / `patch` |
| 9 | Code Executor | Run Python with `execute_code` |
| 10 | Terminal Tyrant | Execute shell commands |

---

### 🏗️ Architect (Vibe-Coding Specialist)
Target: Maximize Vibe Coding and Hermes Native badges

| Priority | Badge | Strategy |
|----------|-------|----------|
| 1 | This Was Supposed To Be Quick | Start a refactor, let it spiral |
| 2 | One More Small Change | Iterate on one file 150+ times |
| 3 | Vibe Architect | Touch many files in one session |
| 4 | Ship First, Ask Later | Git commit + push from Hermes |
| 5 | CSS Exorcist | Frontend projects with styling |
| 6 | Skillsmith | Create skills from coding patterns |
| 7 | Memory Palace | Write memory entries after each session |
| 8 | Context Dragon | Long context sessions with compression |

---

### 🔬 Researcher (Information Forager)
Target: Maximize Research/Web and Model badges

| Priority | Badge | Strategy |
|----------|-------|----------|
| 1 | Rabbit Hole Certified | Deep-dive research with 20+ web calls |
| 2 | Citation Goblin | Use `web_extract` on every source |
| 3 | Docs Archaeologist | Read documentation files |
| 4 | Search Orchestrator | 50+ web calls in one session |
| 5 | Provider Polyglot | Switch models with `/model` |
| 6 | Claude Confidant | Use Anthropic Claude exclusively |
| 7 | Five-Model Flight | Use 5 models in one long session |
| 8 | Open Weights Pilgrim | Run local models via Ollama |

---

### 🤖 Autonomy Engineer (Background Work)
Target: Maximize Agent Autonomy badges

| Priority | Badge | Strategy |
|----------|-------|----------|
| 1 | Let Him Cook | One session with 200+ tool calls |
| 2 | Subagent Commander | Spawn 5+ `delegate_task` children |
| 3 | Background Process Enjoyer | Run `terminal(background=True)` |
| 4 | Cron Necromancer | Schedule jobs with `cronjob` tool |
| 5 | Full Send | Heavy terminal + file + web in one session |
| 6 | Autonomous Avalanche | Just keep using Hermes daily |

---

## 6. API Reference

### Dashboard API Endpoints

```
Base: http://127.0.0.1:9119/api/plugins/hermes-achievements/
```

| Method | Endpoint | Returns |
|--------|----------|---------|
| `GET` | `/achievements` | Full catalog + your progress |
| `GET` | `/scan-status` | Current scan state |
| `GET` | `/recent-unlocks` | Recently earned badges |
| `GET` | `/sessions/{id}/badges` | Badges for a specific session |
| `POST` | `/rescan` | Force full rescan |
| `POST` | `/reset-state` | Wipe all progress |

### Example: Export Progress to JSON

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | {name, tier, progress, unlocked}' > my_progress.json
```

### Example: Check Recent Unlocks

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/recent-unlocks \
  | jq '.[] | {name, tier, unlocked_at}'
```

### State Files (Local)

```
~/.hermes/plugins/hermes-achievements/
├── state.json              # Your unlocks + timestamps
├── scan_snapshot.json      # Cached scan payload
└── scan_checkpoint.json    # Per-session stats cache
```

---

## 7. Training Exercises

### Exercise 1: First Blood + Toolchain Maxxer (30 min)
**Goal:** Unlock 2 badges in one session.

1. Start Hermes: `hermes --tui`
2. Use at least 18 different tools in one session:
   - `web_search`, `web_extract`, `read_file`, `write_file`, `terminal`, `execute_code`, `browser_navigate`, `memory`, `skill_manage`, `delegate_task`, `cronjob`, `todo`, `clarify`, `session_search`, `fact_store`, `image_generate`, `tts`, `vision_analyze`
3. Type `/save` and exit
4. Run: `hermes dashboard` → Achievements tab → verify unlocks

---

### Exercise 2: The Vibe Coding Gauntlet (2 hours)
**Goal:** Unlock 3 Vibe Coding badges.

1. Pick a small project (e.g., a Python script or HTML page)
2. Start: `hermes --tui`
3. Iterate on the file repeatedly:
   - Edit → test → edit → test
   - Aim for 150+ file tool calls
   - Touch 300+ files (create temp files if needed)
4. Let the session run 300+ messages
5. Check dashboard for:
   - This Was Supposed To Be Quick
   - One More Small Change
   - Vibe Architect

---

### Exercise 3: Research Rabbit Hole (1 hour)
**Goal:** Unlock Rabbit Hole Certified and Citation Goblin.

1. Pick a complex topic (e.g., "Qdrant vector search optimization")
2. Use `web_search` 20+ times
3. Use `web_extract` on 10+ sources
4. Use `browser_navigate` to read documentation
5. Create a summary with `write_file`
6. Check dashboard

---

### Exercise 4: Secret Hunter (Ongoing)
**Goal:** Discover all 8 secret achievements.

| Secret | Action |
|--------|--------|
| Port 3000 Is Taken | Start a server, then try to start it again |
| Permission Denied Any% | Run `sudo` commands that fail |
| Forgot The Env Var | Load configs with missing env vars |
| YAML Colon Incident | Edit YAML with syntax errors |
| Docker Name Collision | `docker run --name same_name` twice |
| Rollback Wizard | Use `/rollback` after bad edits |
| One Character Fix | Fix a bug with a 1-char patch |
| Legend | Reach Olympian everywhere |

---

## 8. Achievement Mastery Roadmap

### Phase 1: Beginner (Week 1–2)
**Target:** 15+ badges, mostly Copper/Silver
- First Blood, Centurion (first 100 sessions)
- Red Text Connoisseur, Actually Read The Logs
- Memory Keeper, Memory Palace
- Rabbit Hole Certified, Citation Goblin
- Toolchain Maxxer, Let Him Cook
- Weekend Warrior, Night Owl

### Phase 2: Intermediate (Week 3–6)
**Target:** 30+ badges, Gold tier on favorites
- All Vibe Coding badges
- Subagent Commander, Background Process Enjoyer
- Skillsmith, Skill Issue? Skill Created.
- Provider Polyglot, Claude Confidant/Gemini Cartographer
- File Master, Code Executor, Terminal Tyrant

### Phase 3: Advanced (Month 2–3)
**Target:** 45+ badges, Diamond on core skills
- Cron Necromancer, Full Send
- Autonomous Avalanche, Tool Century
- Context Dragon, Gateway Dweller
- Pixel Goblin, CSS Exorcist
- Marathon Runner (3,000 min session)

### Phase 4: Master (Month 4–6)
**Target:** 55+ badges, Olympian on 10+ achievements
- All Model/Provider badges at Olympian
- All Lifestyle badges at Olympian
- All Secret badges discovered
- Compression Survivor, Checkpoint Champion
- Curator Caller, Memory Packer

### Phase 5: Legend (Month 6+)
**Target:** Legend badge
- Olympian in ALL achievements
- The ultimate Hermes mastery credential

---

## Appendix A: Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                 HERMES ACHIEVEMENTS CHEAT SHEET             │
├─────────────────────────────────────────────────────────────┤
│  9 Categories    │ 60 Badges    │ 5 Tiers                    │
│  8 Secrets       │ 3 Kinds      │ Copper→Silver→Gold→D→O   │
├─────────────────────────────────────────────────────────────┤
│  AUTONOMY     │ 7  │ DEBUGGING  │ 10 │ VIBE CODING │ 7    │
│  HERMES NATIVE│ 8  │ RESEARCH   │ 4  │ MODEL LORE  │ 5    │
│  LIFESTYLE    │ 3  │ SOCIAL     │ 3  │ MILESTONES  │ 16   │
├─────────────────────────────────────────────────────────────┤
│  Dashboard: hermes dashboard → Achievements tab               │
│  API: curl localhost:9119/api/plugins/hermes-achievements/    │
│  Rescan: POST /rescan                                       │
│  Share: PNG share cards (1200×630) on unlocked badges       │
└─────────────────────────────────────────────────────────────┘
```

---

## Appendix B: Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1.x | Early 2026 | Community plugin by PCinkusz |
| v0.2.x | Apr 2026 | 60+ badges, model/provider achievements |
| v0.3.0 | Apr 29 2026 | Snapshot cache + incremental scan |
| v0.4.0 | May 4 2026 | PNG share cards (1200×630) |
| Bundled | Ongoing | Ships with Hermes Agent core |

---

## Appendix C: Related Resources

| Resource | URL |
|----------|-----|
| Hermes Agent Docs | https://hermes-agent.nousresearch.com |
| Achievements Plugin (Upstream) | https://github.com/PCinkusz/hermes-achievements |
| Bundled Plugin (Nous) | https://github.com/NousResearch/hermes-agent/tree/main/plugins/hermes-achievements |
| Community Subreddit | https://reddit.com/r/hermesagent |
| Plugin Ranking (Composio) | https://composio.dev/content/best-hermes-plugins |

---

*Document compiled from live source code analysis, official documentation, and community research. For the exact current state of your achievements, run `hermes dashboard` and visit the Achievements tab.*
