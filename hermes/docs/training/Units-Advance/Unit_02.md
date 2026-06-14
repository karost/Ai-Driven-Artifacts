# Unit 02 — Tool Proficiency
> **Scope:** Autonomy, debugging chaos, and toolchain intensity badges.
> **System:** Hermes Agent v0.15.1  
> **Hardware Context:** 2015 MacBook Pro, 16 GB RAM, macOS Ventura

---

## Lab (Operator-Focused / CLI Hands-On)

### 1. Prerequisites
- Hermes Agent v0.15.1 on a 2015 MacBook Pro (16 GB RAM, macOS Ventura).
- Docker Desktop installed (older builds work on Ventura; allocate ≤4 GB to Docker).
- Python 3.11+ and `jq` available in `PATH`.
- At least Copper tier in `first_blood`.

### 2. Objectives
By the end of this lab you will:
- Trigger tool-intensity badges (`let_him_cook`, `toolchain_maxxer`, `autonomous_avalanche`).
- Safely induce controlled errors for debugging badges (`red_text_connoisseur`, `stack_trace_sommelier`, `yaml_colon_incident`).
- Run background processes and cron jobs to advance autonomy badges.

### 3. Why It Matters
Tool proficiency badges prove you can squeeze maximum value from Hermes on constrained hardware. A 2015 MBP’s thermal envelope tightens under sustained load; learning to background tasks and batch tool calls keeps you productive without fan noise dominating the room.

### 4. Step-by-Step with EXACT Commands

**4.1 Let Him Cook (max tool calls in one session)**
Inside Hermes, issue a rapid chain in a single chat:
```
read_file /tmp/test1.txt
search_files "pattern" *.py
web_search "python list comprehension"
terminal echo hello
execute_code print(2+2)
memory get last_note
skill_manage list
```
Repeat variations until the session exceeds 200 tool calls. Use a scratch workspace to avoid project corruption.

**4.2 Toolchain Maxxer (max distinct tools in one session)**
Explicitly invoke as many unique tool IDs as possible in one conversation:
```
1. web_search
2. web_extract
3. read_file
4. write_file
5. patch
6. search_files
7. terminal
8. execute_code
9. browser_navigate
10. memory
11. skill_manage
12. delegate_task
13. cronjob
14. todo
15. clarify
16. session_search
17. fact_store
18. image_generate
```
Aim for 18+ distinct tools in one session. On a 2015 MBP, stay under 28 distinct tools until memory pressure is comfortable.

**4.3 Background Process Enjoyer**
```bash
# Run a long tail in background via Hermes terminal(<background=True>)
terminal command="tail -f /var/log/system.log" background=True
```
Each background terminal invocation counts. On Ventura, keep ≤3 background logs open to preserve RAM.

**4.4 Cron Necromancer**
```bash
# Schedule a harmless cron that echoes a timestamp
cronjob schedule="*/5 * * * *" command="date >> /tmp/hermes_cron.log"
```
Wait. Each scheduled execution increments the counter. Over a week, 1k executions are easy.

**4.5 Red Text Connoisseur & Stack Trace Sommelier**
Deliberately trigger safe errors inside a controlled Hermes `execute_code`:
```python
# execute_code cell
1/0
```
That raises a `ZeroDivisionError`, counting toward both total errors and traceback events. Repeat 5–10 times in a sandbox notebook.

**4.6 Permission Denied Any%**
```bash
terminal command="sudo ls /root" background=False
```
On a 2015 MBP without root access, this fails with permission denied—earning the badge counter.

**4.7 Port 3000 Is Taken**
```bash
# Terminal 1: start a dummy server
python3 -m http.server 3000
# Terminal 2: try the same port again
python3 -m http.server 3000
```
The second invocation fails with port conflict. Hermes logs this if run via the `terminal` tool.

**4.8 YAML Colon Incident**
Create a malformed YAML via Hermes `write_file`:
```yaml
# /tmp/bad.yaml
key: value: extra_colon
```
Then run a YAML parser:
```bash
terminal command="python3 -c 'import yaml; yaml.safe_load(open(\"/tmp/bad.yaml\"))'"
```
The parser error counts toward the badge.

**4.9 Docker Name Collision**
```bash
terminal command="docker run --name hermes_collision_test hello-world"
terminal command="docker run --name hermes_collision_test hello-world"
```
The duplicate name triggers the Docker conflict event.

### 5. Troubleshooting
| Symptom | Fix |
|---------|-----|
| Docker not found | Install Docker Desktop for Intel Mac (Ventura compatible). |
| `cronjob` tool missing | Ensure `cron` plugin is enabled in `~/.hermes/config.yaml`. |
| Permission denied in Hermes terminal | The error itself is the goal; do not fix it. |
| Background process silently exits | Check `~/Library/Logs/hermes/` for exit codes. |
| Thermal throttling during tool spam | Pause 30 s between bursts; a 2015 MBP needs breath. |

### 6. Expected Outcome
You will earn at least Copper on `let_him_cook`, `toolchain_maxxer`, `red_text_connoisseur`, and `permission_denied_any_percent`. Background and cron counters will begin incrementing.

### 7. Use Case Completed
A DevOps engineer on a 2015 MBP prototypes CI pipelines in Docker. Controlled failures (port collisions, permission denials) naturally populate the debugging badges while background builds advance autonomy badges.

### 8. Training Idea
Create a “badge farm” session template: 20 minutes of deliberate tool chaining, followed by 5 minutes of intentional errors in a sandbox, followed by scheduling three cron jobs. Run the template once per day.

### 9. Challenge
Reach **Gold** on `let_him_cook` (1,200 tool calls in one session) without exceeding 12 GB RAM on your 2015 MBP. Hint: use lightweight tools like `terminal` and `read_file` rather than heavy `browser_navigate` or `image_generate` calls.

### 10. Emotional Reward
The first time your Dashboard flashes a Diamond-tier `red_text_connoisseur`, you smile—because every crash was a lesson you chose to learn.

---

## Chapter (Architect-Focused / Code & Internals)

### 1. Top Objectives
- Understand how the scan engine classifies tool calls, errors, and background events.
- Build a local dashboard widget that surfaces today’s autonomy + debugging delta.
- Design a “safe failure sandbox” that earns badges without destabilizing macOS Ventura.

### 2. Description
Agent Autonomy and Debugging Chaos contain 17 badges (7 + 10) focused on tool-call volume, diversity, background execution, cron usage, and a wide spectrum of error events. The plugin listens to session events in `~/.hermes/state.db` and maps each event to an achievement metric. On a 2015 MBP, the scan engine’s incremental checkpointing is critical because full SQLite rescans would block the UI for seconds.

### 3. Actions List
1. Open `state.db` in a read-only SQLite client to inspect raw events.
2. Map `tool_type` rows to badge categories.
3. Filter `error_message` rows to count unique error classes.
4. Export daily deltas for autonomy badges.
5. Build a macOS Notification Center script that fires on tier promotion.

### 4. Full Source Code Snippet with Line-by-Line Explanations
```python
#!/usr/bin/env python3
# badge_delta.py — run daily on a 2015 MBP; reads API, prints deltas
import requests, json, os
from datetime import datetime

API = "http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements"
SNAP = os.path.expanduser("~/.hermes/badge_snapshot.json")

# Line 1: Load prior snapshot (or seed empty)
old = {}
if os.path.exists(SNAP):
    with open(SNAP) as f:
        old = json.load(f)

# Line 2: Fetch current progress
curr = {a["id"]: a for a in requests.get(API).json()["achievements"]}

# Line 3: Compute deltas for target badges
targets = [
    "let_him_cook","autonomous_avalanche","toolchain_maxxer",
    "subagent_commander","background_process_enjoyer","cron_necromancer",
    "red_text_connoisseur","stack_trace_sommelier",
    "port_3000_taken","permission_denied_any_percent",
    "docker_name_collision","yaml_colon_incident"
]
report = []
for tid in targets:
    a = curr.get(tid)
    if not a:
        continue
    prev = old.get(tid, {}).get("progress", 0)
    delta = a["progress"] - prev
    if delta > 0:
        report.append(f"{tid}: +{delta} → {a['tier']}")

# Line 4: Write new snapshot atomically
with open(SNAP, "w") as f:
    json.dump({k: {"progress": v["progress"], "tier": v["tier"]} for k,v in curr.items()}, f)

# Line 5: Print report
print(datetime.now().isoformat())
print("\n".join(report) or "No badge progress today.")
```
- **Line 1:** Storing yesterday’s snapshot lets us compute daily change without querying the Dashboard UI.
- **Line 2:** The API returns a flat achievement list; we index by ID for fast lookup.
- **Line 3:** Only the 12 key badges are tracked here; expand the list as desired.
- **Line 4:** Atomic JSON write avoids corruption if the script is killed mid-save.
- **Line 5:** A concise report suitable for a macOS `say` command or Notification Center bridge.

### 5. Master Prompt (Ready-to-Copy for Kimi-K2.6)
```
You are a Hermes Agent coach. The user is working on Unit 02: Tool Proficiency.
They run Hermes v0.15.1 on a 2015 MacBook Pro with 16 GB RAM.

Task:
1. List the 17 Agent Autonomy + Debugging Chaos badge IDs and their Copper thresholds.
2. Design a single 30-minute “badge farm” Hermes session that advances at least 6 distinct badges safely on a low-RAM machine.
3. Indicate which tools to avoid during the session to prevent thermal throttling.
4. Provide a Python snippet that posts a macOS notification when a tier changes.
5. End with a one-line zsh alias to run the badge-delta script.
```

### 6. Conclusion
- `let_him_cook` is gated by session peak, not lifetime—use one long intense chat rather than spreading calls thin.
- `toolchain_maxxer` requires tool diversity; memorize the full tool palette to avoid duplicates.
- Background and cron badges are passive growers: set them up once, let time do the work.
- Debugging badges reward resilience on a 2015 MBP because older hardware sees more resource contention (port collisions, permission issues, Docker naming).
- The incremental scan engine keeps Dashboard performance steady even as error/event counts climb into the thousands.

### 7. Architecture Note
Event classification happens in `plugin_api.py`. Each row in `state.db` carries a `tool_type` and optional `error_message`. The plugin’s `AchievementEvaluator` maps regex patterns (e.g., `port.*already in use`) to badge counters. Because the scan is incremental, newly saved sessions append to the checkpoint rather than reprocessing all history.

### 8. Integration Checklist
- [ ] At least 18 distinct tools invoked in a single session.
- [ ] One controlled permission-denied event logged.
- [ ] Background process started via `terminal(background=True)`.
- [ ] Cron job scheduled and executed successfully.
- [ ] `badge_delta.py` prints non-empty report after a session.

---

## Questions
1. What is the Copper threshold for `let_him_cook`, and what `kind` does it use?
2. How many total distinct tools must be used in one session to reach Gold tier in `toolchain_maxxer`?
3. On a 2015 MacBook Pro with 16 GB RAM, why should you avoid heavy tools while grinding `let_him_cook`?
4. Which two badges in this unit are `multi_condition` rather than simple lifetime counters?
5. What macOS file path stores the badge progress snapshot between daily delta runs?
