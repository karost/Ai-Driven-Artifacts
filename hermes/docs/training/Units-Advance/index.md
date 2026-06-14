# Advance Track — Achievements Deep-Dive: Navigation Index

> **Hermes Version:** v0.15.1 — Live CLI & Source Code Verified  
> **Hardware Context:** macOS Ventura, Intel x86_64 (MacBook Pro 2015, 16 GB RAM)  
> **Status:** 9 Units Complete — All 60+ Badges Covered  
> **Total Size:** ~132 KB across 9 files  
> **Prerequisite:** Units-Basic 1–5 (or equivalent CLI competence)  
> **Date:** June 2026

---

## Quick Start

1. **New to achievements?** → Start at **[Unit_01.md](Unit_01.md)** — Usage Milestones.
2. **Know the dashboard already?** → Pick any unit below by category.
3. **Want the secret badges?** → Jump to **[Unit_09.md](Unit_09.md)** — Secret Achievements.
4. **Need the full deep reference?** → [`docs/hermes-achievements-training.md`](../hermes-achievements-training.md)

---

## Unit Map

| Unit | Category | Badges | Level | Est. Time | File |
|------|----------|--------|-------|-----------|------|
| **01** | **Usage Milestones** | `first_blood`, `centurion`, `marathon_runner`, `tool_century`, `file_master`, `code_executor`, `terminal_tyrant`, `web_wanderer`, `vision_seeker`, `tts_bard`, `image_gen_artisan`, `compression_survivor`, `checkpoint_champion`, `memory_packer`, `curator_caller`, `legend` | Beginner | ~60 min | [Unit_01.md](Unit_01.md) |
| **02** | **Tool Proficiency** | `let_him_cook`, `autonomous_avalanche`, `toolchain_maxxer`, `full_send`, `subagent_commander`, `background_process_enjoyer`, `cron_necromancer`, `red_text_connoisseur`, `stack_trace_sommelier`, `actually_read_the_logs`, `port_3000_taken`, `permission_denied_any_percent`, `dependency_hell_tourist`, `the_fix_was_restarting`, `forgot_the_env_var`, `yaml_colon_incident`, `docker_name_collision` | Intermediate | ~85 min | [Unit_02.md](Unit_02.md) |
| **03** | **Model Diversity** | `five_model_flight`, `provider_polyglot`, `claude_confidant`, `gemini_cartographer`, `open_weights_pilgrim` | Beginner | ~50 min | [Unit_03.md](Unit_03.md) |
| **04** | **Memory & Research** | `rabbit_hole_certified`, `citation_goblin`, `docs_archaeologist`, `search_orchestrator`, `memory_keeper`, `memory_palace`, `context_dragon` | Intermediate | ~75 min | [Unit_04.md](Unit_04.md) |
| **05** | **Skills & Automation** | `skillsmith`, `skill_issue_skill_created`, `memory_keeper`, `memory_palace`, `context_dragon`, `gateway_dweller`, `plugin_goblin`, `rollback_wizard`, `subagent_commander`, `cron_necromancer`, `background_process_enjoyer` | Intermediate | ~80 min | [Unit_05.md](Unit_05.md) |
| **06** | **Error & Recovery** | `red_text_connoisseur`, `stack_trace_sommelier`, `actually_read_the_logs`, `port_3000_taken`, `permission_denied_any_percent`, `dependency_hell_tourist`, `the_fix_was_restarting`, `forgot_the_env_var`, `yaml_colon_incident`, `docker_name_collision` | Intermediate | ~90 min | [Unit_06.md](Unit_06.md) |
| **07** | **Session Quality** | `weekend_warrior`, `night_owl`, `early_bird_cron`, `supposed_to_be_quick`, `one_more_small_change`, `vibe_architect`, `marathon_runner` | Intermediate | ~70 min | [Unit_07.md](Unit_07.md) |
| **08** | **Social & Community** | `shared_session`, `team_delegate`, `cross_platform` | Beginner | ~45 min | [Unit_08.md](Unit_08.md) |
| **09** | **Secret Achievements** | `port_3000_taken`, `permission_denied_any_percent`, `forgot_the_env_var`, `yaml_colon_incident`, `docker_name_collision`, `rollback_wizard`, `one_character_fix`, `legend` | Advanced | ~100 min | [Unit_09.md](Unit_09.md) |

---

## Playstyle Paths

### 🚀 Speedrun Path (5 badges in 30 minutes)
1. **[Unit_01](Unit_01.md)** Lab 1 — Check dashboard, confirm `first_blood`
2. **[Unit_03](Unit_03.md)** Lab 3 — Switch 5 models, trigger `provider_polyglot` (Copper)
3. **[Unit_04](Unit_04.md)** Lab 1 — Run 5 web searches, trigger `rabbit_hole_certified`
4. **[Unit_05](Unit_05.md)** Lab 1 — Create one skill, trigger `skill_issue_skill_created`
5. **[Unit_08](Unit_08.md)** Lab 1 — Export session, trigger `shared_session`

### 🏗️ Architect Path (Understand every engine)
1. **[Unit_01](Unit_01.md)** Chapter — Session counter pipeline, state.json format
2. **[Unit_02](Unit_02.md)** Chapter — Tool call detection, classification logic
3. **[Unit_04](Unit_04.md)** Chapter — Research tracker, SQL aggregation
4. **[Unit_05](Unit_05.md)** Chapter — Skill plugin lifecycle, cron event routing
5. **[Unit_09](Unit_09.md)** Chapter — Secret classifier, Legend bulk evaluation

### 🎯 Legend Path (Reach Olympian everywhere)
1. Complete **all 9 units** in order
2. Follow the phase roadmap in [Unit_09](Unit_09.md) §Legend Phase
3. Track with: `curl .../achievements | jq '[.achievements[] | select(.tier == "olympian")] | length'`

---

## Structure (Every Unit)

| Section | What It Contains |
|---------|-----------------|
| **Lab** | Operator hands-on — CLI commands, dashboard API, tier grinding |
| **Chapter** | Architect analysis — source code, engine internals, annotated pseudo-code |
| **Master Prompt** | Ready-to-copy for Kimi-K2.6 / Claude / GPT |
| **5 Questions** | Active recall — test understanding |

**Each unit:** ~250–480 lines, ~11–20 KB  
**Scaffolding:** 10 Lab elements + 8 Chapter elements + 5 Questions = 23 points per unit  
**Hardware context:** Referenced throughout (2015 Mac thermal limits, RAM constraints)

---

## Related Files

| File | What It Is |
|------|-----------|
| [`Units-Basic/index.md`](../Units-Basic/index.md) | Core Hermes training (20 Units) |
| [`hermes-achievements-training.md`](../hermes-achievements-training.md) | Deep reference manual (500+ lines, all 60 badges with full thresholds) |
| [`Hermes-Agent-Advance-Handbook.md`](../Hermes-Agent-Advance-Handbook.md) | Handbook overview — the complete achievement system in one file |

---

## File Tree

```
docs/training/
├── Units-Basic/              ← 20 Units (core Hermes training)
├── Units-Advance/            ← 9 Units (achievements deep-dive)
│   ├── index.md              ← THIS FILE
│   ├── Unit_01.md            ← Usage Milestones
│   ├── Unit_02.md            ← Tool Proficiency
│   ├── Unit_03.md            ← Model Diversity
│   ├── Unit_04.md            ← Memory & Research
│   ├── Unit_05.md            ← Skills & Automation
│   ├── Unit_06.md            ← Error & Recovery
│   ├── Unit_07.md            ← Session Quality
│   ├── Unit_08.md            ← Social & Community
│   └── Unit_09.md            ← Secret Achievements
├── Hermes-Agent-Advance-Handbook.md  ← Overview handbook
└── hermes-achievements-training.md     ← Deep reference (60 badges)
```

---

*Built for Thanit Tritrang. Tested on a 2015 MacBook Pro. Verified against Hermes v0.15.1. May your agent learn long and well.*
