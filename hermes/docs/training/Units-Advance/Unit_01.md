# Unit 01 — Usage Milestones
> **Scope:** Lifetime counters and endgame mastery badges.
> **System:** Hermes Agent v0.15.1  
> **Hardware Context:** 2015 MacBook Pro, 16 GB RAM, macOS Ventura

---

## Lab (Operator-Focused / CLI Hands-On)

### 1. Prerequisites
- Hermes Agent v0.15.1 running on a 2015 MacBook Pro (16 GB RAM, macOS Ventura).
- At least one completed session (`first_blood` already earned).
- Terminal with `curl` and `jq` installed.
- Dashboard reachable at `http://127.0.0.1:9119`.
- Optional: Python 3.11+ for the local tracker script.

### 2. Objectives
By the end of this lab you will:
- Read your Milestones & Mastery tier progress via the Dashboard API.
- Understand the exact thresholds for `centurion`, `tool_century`, `file_master`, `terminal_tyrant`, and `legend`.
- Map daily workflows to the 16 milestone badges.

### 3. Why It Matters
Milestone badges are **lifetime counters**. They represent the backbone of your Legend run. On a 2015 MBP with 16 GB RAM, you will hit IO and thermal limits before hitting badge limits—so knowing which workflows to batch (file ops, terminal commands, web calls) prevents throttling while grinding tiers.

### 4. Step-by-Step with EXACT Commands

**4.1 Badge Tier Reference Table**

| ID | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|---|---|---|---|---|---|---|---|
| `first_blood` | `lifetime` | First session completed | 1 | — | — | — | — |
| `centurion` | `lifetime` | Total sessions | 100 | 300 | 1,000 | 3,000 | 10,000 |
| `marathon_runner` | `best_session` | Longest session (minutes) | 60 | 180 | 480 | 1,200 | 3,000 |
| `tool_century` | `lifetime` | Total tool calls | 10k | 30k | 100k | 300k | 1M |
| `file_master` | `lifetime` | File operations | 5k | 15k | 50k | 150k | 500k |
| `code_executor` | `lifetime` | `execute_code` runs | 1k | 3k | 10k | 30k | 100k |
| `terminal_tyrant` | `lifetime` | Terminal commands | 2k | 6k | 20k | 60k | 200k |
| `web_wanderer` | `lifetime` | Web search/extract | 5k | 15k | 50k | 150k | 500k |
| `vision_seeker` | `lifetime` | Vision/image analysis | 100 | 300 | 1,000 | 3,000 | 10,000 |
| `tts_bard` | `lifetime` | Text-to-speech uses | 50 | 150 | 500 | 1,500 | 5,000 |
| `image_gen_artisan` | `lifetime` | Image generations | 50 | 150 | 500 | 1,500 | 5,000 |
| `compression_survivor` | `lifetime` | Context compressions | 10 | 30 | 100 | 300 | 1,000 |
| `checkpoint_champion` | `lifetime` | Checkpoints created | 50 | 150 | 500 | 1,500 | 5,000 |
| `memory_packer` | `lifetime` | Memory consolidations | 10 | 30 | 100 | 300 | 1,000 |
| `curator_caller` | `lifetime` | Curator invocations | 5 | 15 | 50 | 150 | 500 |
| `legend` | `multi_condition` | ALL metrics at Olympian | — | — | — | — | — |

**4.2 Check your current milestone progress**
```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | select(.category == "Milestones & Mastery") | {id, tier, progress, threshold}'
```

**4.3 Verify First Blood**
```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | select(.id == "first_blood")'
```

**4.4 Simulate a Centurion push**
Start a session and run a lightweight workload loop (safe on 2015 MBP):
```bash
for i in {1..25}; do
  echo "session_batch_$i" >> /tmp/hermes_centurion_log.txt
done
```
Each saved session counts toward `centurion`. On Ventura, 25 sessions can be completed in one afternoon without swap pressure.

**4.5 Batch tool calls for Tool Century**
Inside a single Hermes session, chain small `read_file`, `search_files`, and `terminal` tasks. Each tool invocation increments the `tool_century` counter. Aim for 500+ calls across a week.

**4.6 File Master grind**
```bash
# Create a scratch directory and churn file ops
mkdir -p /tmp/hermes_file_master
for i in {1..50}; do
  touch /tmp/hermes_file_master/f_$i.txt
  echo "data" > /tmp/hermes_file_master/f_$i.txt
done
```
Use Hermes `write_file` and `patch` on these scratch files rather than project code.

**4.7 Terminal Tyrant via safe loops**
```bash
# Run 100 harmless echo commands in one Hermes terminal() call
for n in {1..100}; do echo "term_line_$n"; done
```

**4.8 Web Wanderer basics**
```bash
# Use Hermes web_search and web_extract inside a research session
# Example trigger inside Hermes:
web_search query="python asyncio best practices"
web_extract url="https://docs.python.org/3/library/asyncio.html"
```

**4.9 Code Executor micro-runs**
```python
# Inside execute_code
for i in range(50):
    print(f"exec_batch_{i}")
```

### 5. Troubleshooting
| Symptom | Fix |
|---------|-----|
| Dashboard 404 | Ensure Hermes is running: `hermes dashboard` |
| Empty progress | Run a new session, type `/save`, then `POST /rescan` |
| API returns `null` | Wait for first background scan to finish (~30 s on 2015 SSD) |
| Legend not appearing | Secret; remains hidden until all other tiers are Olympian |
| High fan noise during batch | Pause 10 s between bursts; 2015 MBP thermal guard is aggressive |
| Swap pressure | Quit Safari tabs; use `terminal` instead of `browser_navigate` |

### 6. Expected Outcome
You will see JSON output showing tiers from `Copper` to `Olympian` and your numeric progress. At minimum, `first_blood` shows `tier: "Copper"`.

### 7. Use Case Completed
A solo developer on a 2015 MBP wants to track productive weeks. Centurion Gold (1,000 sessions) proves ~2 years of daily usage.

### 8. Training Idea
Mount a weekly ritual: Sunday evening, run the API curl, log progress in a markdown note. Watching the numbers tick up is a powerful motivator.

### 9. Challenge
Reach **Silver tier** on `centurion`, `file_master`, and `terminal_tyrant` within 14 days without exceeding 80 % memory pressure on your 2015 machine.

### 10. Emotional Reward
The first time you see a Gold tier badge shimmer in the Dashboard, you realize the grind was the feature.

---

## Chapter (Architect-Focused / Code & Internals)

### 1. Top Objectives
- Map the Milestone achievement schema to the scan engine.
- Reproduce tier-threshold evaluation logic.
- Build a local monitoring script using the public API.

### 2. Description
Milestones & Mastery contains 16 lifetime achievements tracked by the `hermes-achievements` plugin. Each badge uses a `lifetime` kind (cumulative) except `marathon_runner` (`best_session` / peak minutes) and `legend` (`multi_condition`). On low-memory hosts like a 2015 MacBook, the scan engine avoids full-history reloads by using `SNAPSHOT_TTL_SECONDS = 120` and a checkpoint cache.

### 3. Actions List
1. Query `/achievements` and filter by category.
2. Parse tier thresholds from the `thresholds` map.
3. Compute remaining progress: `next_threshold - current_progress`.
4. Export a weekly CSV for trend tracking.
5. Alert when a tier boundary is crossed.

### 4. Full Source Code Snippet with Line-by-Line Explanations
```python
#!/usr/bin/env python3
# milestone_tracker.py — safe to run on a 2015 MBP with 16 GB RAM
import requests, json, csv, os

BASE = "http://127.0.0.1:9119/api/plugins/hermes-achievements"

# Line 1: Fetch the full catalog + user progress
resp = requests.get(f"{BASE}/achievements")
resp.raise_for_status()

# Line 2: Parse JSON payload
data = resp.json()

# Line 3: Filter milestone badges
milestones = [a for a in data["achievements"]
              if a.get("category") == "Milestones & Mastery"]

# Line 4: Prepare CSV rows for weekly tracking
rows = []
for badge in milestones:
    tid = badge["id"]
    progress = badge.get("progress", 0)
    tier = badge.get("tier", "None")
    # thresholds is a dict: {"copper": n, "silver": n, ...}
    thresholds = badge.get("thresholds", {})
    next_key = None
    for t in ["copper","silver","gold","diamond","olympian"]:
        if t != tier.lower() and thresholds.get(t, 0) > progress:
            next_key = t
            break
    remaining = (thresholds.get(next_key, 0) - progress) if next_key else 0
    rows.append([tid, tier, progress, next_key or "max", remaining])

# Line 5: Write CSV to disk (append mode for weekly logging)
out = os.path.expanduser("~/hermes_milestone_log.csv")
with open(out, "a", newline="") as f:
    writer = csv.writer(f)
    for r in rows:
        writer.writerow(r)

print(f"Logged {len(rows)} milestones to {out}")
```
- **Line 1:** The catalog endpoint returns achievements merged with user state.
- **Line 2:** `data["achievements"]` is a flat list of dicts.
- **Line 3:** We keep only the 16 Milestone badges to keep memory low.
- **Line 4:** Tier thresholds come from the server so the script never hard-codes values.
- **Line 5:** Appending to CSV avoids rewriting large files; ideal for spinning HDDs on older Macs.

### 5. Master Prompt (Ready-to-Copy for Kimi-K2.6)
```
You are a Hermes Agent coach. The user is working on Unit 01: Usage Milestones.
They run Hermes v0.15.1 on a 2015 MacBook Pro with 16 GB RAM.

Task:
1. List the 16 Milestone badge IDs and their Copper thresholds.
2. Identify which 3 badges are easiest to reach Gold tier on a low-RAM machine.
3. Output a 14-day daily ritual (≤15 min/day) that advances centurion, file_master, and terminal_tyrant without thermal throttling.
4. Include the exact curl command to check progress.
5. End with a one-line CLI alias the user can paste into ~/.zshrc.
```

### 6. Conclusion
- Milestones reward consistency, not speed. A 2015 MBP is perfectly capable of grinding them if you batch work.
- `tool_century` and `file_master` are the two highest-count badges; optimize by using Hermes tools instead of manual CLI.
- `marathon_runner` requires session stamina, not CPU—leave a long-running research session open overnight.
- `legend` is secret and only appears after all other achievements hit Olympian; treat it as a 6–12 month horizon.
- Use the API to export CSV logs so you can visualize trends without keeping the Dashboard open.

### 7. Architecture Note
The plugin stores progress in `~/.hermes/plugins/hermes-achievements/state.json`. On macOS Ventura with a SATA SSD, writing small JSON deltas every session keeps disk health high and avoids the heavy I/O of a full SQLite rewrite.

### 8. Integration Checklist
- [ ] API returns valid JSON on `curl` probe.
- [ ] `state.json` exists and updates after `/save`.
- [ ] Weekly CSV logger script runs without memory warnings.
- [ ] Dashboard renders tier icons correctly in Safari / Chrome on macOS Ventura.
- [ ] `first_blood` shows `unlocked: true`.

---

## Questions
1. What is the `kind` tracking type for `centurion`, and how does it differ from `marathon_runner`?
2. How many total sessions are required to reach Olympian tier in `centurion`?
3. On a 2015 MacBook Pro with 16 GB RAM, why is batching tool calls preferable to many short sessions for `tool_century`?
4. What specific condition must be met before the `legend` badge becomes visible?
5. What `jq` filter selects only Milestones & Mastery achievements from the `/achievements` endpoint?
