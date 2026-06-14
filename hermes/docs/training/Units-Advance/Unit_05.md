# Unit 5: Skills & Automation — Procedural Memory, Plugins, Cron, and Subagents

> **Badges covered:** `skillsmith`, `skill_issue_skill_created`, `memory_keeper`, `memory_palace`, `context_dragon`, `gateway_dweller`, `plugin_goblin`, `rollback_wizard`, `subagent_commander`, `cron_necromancer`, `background_process_enjoyer`

## Lab 5: Automation Gauntlet — Skills, Plugins, Cron, and Delegated Subagents

Level: Advanced  
Estimated Time: ~100 minutes  
Prerequisites: Units 1–4 complete (memory, research, model switching).

### Lab Objectives

By the end of this lab you will be able to:

- Create a new skill from scratch using the `skill_manage` tool to unlock `skillsmith` and `skill_issue_skill_created`.
- View and manage skills via `hermes skills list` and `/skills`.
- Install a plugin from the community registry to progress `plugin_goblin`.
- Trigger a rollback with the `/rollback` command to unlock `rollback_wizard`.
- Spawn a delegated subagent with `delegate_task` to progress `subagent_commander`.
- Create a cron job using the `cronjob` tool to advance `cron_necromancer`.
- Run a background process via `terminal(background=True)` for `background_process_enjoyer`.
- Send a message through the gateway (Telegram/Discord/Slack) if configured for `gateway_dweller`.

### Why This Lab Matters

This is the "let the agent run independently" lab. On a 2015 MacBook Pro, background processes and cron jobs are how you keep Hermes productive while you sleep. Skills are procedural memory — the agent remembers HOW to do things. Plugins extend what Hermes can touch. Subagents parallelize work. This lab turns a chatbot into an autonomous system.

### Step-by-Step Instructions

#### Step 1: Skill Forge — Create a Reusable Skill (15 minutes)

Start a fresh session:

```bash
hermes --new
```

Type this exact prompt:

```
Create a skill named "macbook_health_check" that:
1. Runs a Python script to check CPU temperature via osx-cpu-temp
2. Checks free RAM with psutil
3. Checks free disk space with shutil.disk_usage
4. Returns a formatted health report
Save it with skill_manage.
```

Approve all tool calls. When it finishes, verify:

```bash
hermes skills list | grep macbook
```

Check `/skills` inside the chat as well.

**Troubleshooting:** If `skill_manage` is not available, the agent may have auto-extracted the skill. Look for it in `~/.hermes/skills/macbook_health_check.md`. If missing, create it manually:

```bash
cat > ~/.hermes/skills/macbook_health_check.md << 'EOF'
---
name: macbook_health_check
description: Checks 2015 MacBook Pro health metrics
trigger: "health", "thermal", "ram", "disk"
version: 1.0
---

1. Run Python to collect metrics
2. Format a human-readable report
3. Suggest actions if metrics are concerning
EOF
```

#### Step 2: Trigger Skill Reuse (5 minutes)

In the same session, type:

```
Run a health check on my MacBook.
```

If the skill triggers correctly, the agent should ask to execute the Python script without you describing it again. This is `skillsmith` in action.

#### Step 3: Install a Plugin (10 minutes)

From Terminal:

```bash
hermes plugin list
```

Pick any available plugin (e.g., `web_search_advanced`, `screenshot`, `code_runner`). Install it:

```bash
hermes plugin install screenshot
```

Verify with:

```bash
hermes plugin list | grep screenshot
```

Each install counts toward `plugin_goblin` (Copper at 1,000 lifetime plugin events). If you are already past Copper, every new install edges you closer.

#### Step 4: Rollback After a Bad Edit (10 minutes)

Inside the chat, intentionally request a destructive change:

```
Delete every file in ~/tmp_test_folder/. Do it now.
```

(Only do this if `~/tmp_test_folder/` exists and contains disposable files.)

After confirming deletion, type:

```
/rollback
```

Hermes should restore the last checkpoint. Repeat rollbacks 5+ times across the session.

**Alternative path if rollback is unavailable:**
Use the `patch` tool to make a change, then revert it with `patch` again. Some scanners count manual patches toward `rollback_wizard`.

#### Step 5: Delegate a Task to a Subagent (15 minutes)

Type:

```
delegate_task: {
  "task": "Research the current top 3 Python web frameworks in 2026. Return a bullet summary.",
  "timeout": 120,
  "tools": ["web_search", "web_extract"]
}
```

Approve the delegation. Wait for the subagent to return.

Repeat with a second task:

```
delegate_task: {
  "task": "Summarize our memory entries in category 'research'.",
  "timeout": 60,
  "tools": ["memory"]
}
```

Every `delegate_task` counts toward `subagent_commander` (Copper at 5 lifetime).

#### Step 6: Create a Cron Job (15 minutes)

From Terminal:

```bash
hermes cron list
```

Add a simple cron job:

```bash
hermes cron add --name "daily_log" --schedule "0 9 * * *" --command "echo 'Hermes alive at $(date)' >> ~/.hermes/cron_log.txt"
```

Verify it appears in the list. This advances `cron_necromancer` (Copper at 1,000 lifetime cron calls).

On a 2015 MacBook, cron jobs are lightweight. Even an overworked old CPU can handle a single echo every morning.

#### Step 7: Run a Background Process (10 minutes)

Inside the chat, type:

```
terminal: {"command": "ping -c 20 8.8.8.8", "background": true}
```

Hermes should return a session ID. Poll it a minute later:

```
Check background process status for the session ID you gave me.
```

This counts toward `background_process_enjoyer` (Copper at 300 lifetime).

#### Step 8: Memory Housekeeping (5 minutes)

Write 3 structured memory entries:

```
memory: {"action": "save", "category": "automation", "content": "Installed screenshot plugin and tested cron at 09:00 daily."}
```

```
memory: {"action": "save", "category": "automation", "content": "Delegated two subagent tasks: Python frameworks research + research memory summary."}
```

```
memory: {"action": "save", "category": "automation", "content": "Created macbook_health_check skill v1.0 and triggered reuse successfully."}
```

These feed `memory_keeper` + `memory_palace`.

### Expected Outcome

- At least 1 new skill created and verified in `~/.hermes/skills/`.
- At least 1 plugin installed and visible in `hermes plugin list`.
- At least 5 `delegate_task` calls completed (target: Copper).
- At least 1 cron job scheduled.
- At least 1 background process executed.
- 3+ memory entries saved.
- Dashboard shows increased progress on multiple automation badges.

### Lab 5 Use Case Completed

You transformed Hermes from a chat interface into an automation platform. It has procedural memory (skills), extensibility (plugins), scheduling (cron), parallelism (subagents), and background execution (terminal). On a 2015 MacBook Pro, this means the machine works while you sleep.

### Training Idea / Self-Improvement Focus

- Skills you create in this lab may be promoted by the Curator if they are reused frequently.
- Cron jobs run in the macOS cron daemon. Check `/usr/bin/crontab -l` to see Hermes entries.
- Background processes use asyncio Tasks under the hood. On Ventura, you can inspect them with `ps -ax | grep hermes`.
- Subagent delegation isolates context — each subagent gets its own memory slice. This protects your main session from context pollution.

### Challenge (Recommended)

1. Chain a cron job to a skill: schedule `macbook_health_check` to run every morning at 08:00 and write the result to a memory entry.
2. Delegate 5 tasks in a single session to hit `subagent_commander` Copper in one shot.
3. Check if the gateway is active: type `/gateway status` and send a test message to Telegram/Discord if configured.
4. Export your skill to Git:
   ```bash
   cd ~/.hermes/skills && git init && git add . && git commit -m "Lab 5 skills"
   ```

### Emotional Reward

🏆 Your 2015 MacBook Pro now runs an autonomous agent empire. Skills, plugins, cron jobs, subagents, and background processes — you are no longer chatting. You are commanding.

---

## Chapter 5: The Automation Stack — Skills, Curator, and Plugin Lifecycle

**Top Ideal Study Objectives:**
- Trace a skill from markdown file to execution trigger.
- Understand the Curator's 7-day review cycle for skill promotion/pruning.
- Map plugin events to the `plugin_goblin` metric.
- See how cron, background processes, and subagents share the same asyncio loop.

**Description:**
This chapter reveals the architecture beneath Lab 5. We explore how skills become reusable, how the Curator decides what stays and what goes, and why every plugin install is tracked. If Lab 5 was operating the controls, this chapter is reading the schematics.

**Actions List (Topics):**
1. Read a skill Markdown file from `~/.hermes/skills/`.
2. Find the Curator's schedule in `~/.hermes/config.yaml`.
3. Inspect `plugin_api.py` for install hooks.
4. Trace `delegate_task` isolation in the source tree.

**Full Source Code Snippets with Line-by-Line Explanations:**

```python
# automation_stack.py  --  Educational pseudocode for skills, plugins, cron, subagents
# Version: v0.15.1+

"""
Automation Stack orchestrator.

Handles:
  - Skill load / parse / trigger matching
  - Plugin install / uninstall / event hooks
  - Cron job registration via macOS crontab
  - Subagent fork with isolated context
  - Background process delegation

Everything runs on the same asyncio event loop so a 2015 MacBook
with 16GB RAM does not spawn a new OS process per subagent.
"""

import asyncio                 # Line ~15  --  shared loop for all async work
import yaml                    # Line ~16  --  frontmatter parsing in skills
import sqlite3                 # Line ~17  --  plugin state persistence
import subprocess              # Line ~18  --  cron and background shell
from pathlib import Path       # Line ~19  --  skill path resolution

# Line-by-line:
# asyncio   : Subagents and background processes are asyncio Tasks, not
#             OS processes. This keeps RAM usage below ~500MB even with
#             5 concurrent subagents on a 2015 MacBook.
# yaml      : Skill files use YAML frontmatter (--- \n key: value ...). The
#             parser extracts triggers, version, and description before
#             reading the markdown body.
# sqlite3   : Plugin metadata (installed, enabled, version) is stored in
#             plugin_registry.db so Hermes can list and track events.
# subprocess : Cron uses the macOS crontab command. Background shell jobs
#             use subprocess.Popen so output can be streamed back.
# Path      : Skills are resolved relative to ~/.hermes/skills/. Path
#             ensures cross-platform compatibility (macOS Ventura here).

# ---- Skill trigger matching ----
# Called by the agent loop when user speech matches a skill trigger.

def match_skill(user_input: str, skills_dir: Path) -> dict | None:
    for skill_path in skills_dir.glob("*.md"):            # Line ~30
        with open(skill_path, "r") as f:
            frontmatter = yaml.safe_load(f.read())       # Line ~32
        triggers = frontmatter.get("trigger", "")          # Line ~33
        if any(t in user_input.lower() for t in triggers.split(",")):
            return frontmatter                              # Line ~35
    return None                                            # Line ~36

# Line ~30 : Iterates over every .md file in ~/.hermes/skills/. On a
#            2015 MacBook, 50 skills load in <10ms from SSD.
# Line ~33 : Trigger is a comma-separated string in YAML. Example:
#            trigger: "health, thermal, ram, disk"
# Line ~35 : Returns the entire skill definition so the agent can
#            inject the body into the next model prompt.

# ---- Plugin install hook ----
# Called by `hermes plugin install <name>`.

async def install_plugin(name: str) -> str:
    url = f"https://agentskills.io/plugins/{name}.zip"    # Line ~42
    download = await asyncio.to_thread(_download, url)   # Line ~43
    extract_path = Path(f"~/.hermes/plugins/{name}")     # Line ~44
    await asyncio.to_thread(_extract, download, extract_path)  # Line ~45
    _record_plugin_event(name, "install")                  # Line ~46
    return f"Plugin {name} installed."                   # Line ~47

# Line ~42 : Community plugins are hosted on agentskills.io. The URL
#            pattern is stable.
# Line ~43 : asyncio.to_thread() moves blocking network I/O off the
#            main event loop. This prevents UI freeze on old Macs.
# Line ~46 : _record_plugin_event increments the plugin_goblin metric
#            in state.json. Every install, enable, disable counts.

# ---- Cron registration (macOS) ----
# Writes a crontab line for the Hermes user.

def add_cron(name: str, schedule: str, cmd: str) -> None:
    entry = f"{schedule} {cmd} # hermes-cron:{name}\n"     # Line ~54
    existing = subprocess.getoutput("crontab -l")          # Line ~55
    if name not in existing:                              # Line ~56
        new_crontab = existing + "\n" + entry               # Line ~57
        subprocess.run(["crontab", "-"], input=new_crontab, text=True)  # Line ~58

# Line ~54 : Hermes tags each crontab line with a comment so it can
#            identify its own entries later. Example:
#            0 9 * * * echo ... # hermes-cron:daily_log
# Line ~58 : Uses stdin to pipe the new crontab. This is safer than
#            appending to a file directly.

# ---- Subagent isolation ----
# delegate_task creates a new HermesState with a blank memory slice.

async def fork_subagent(task: str, tools: list, timeout: int) -> str:
    child_state = HermesState.new_clone(parent=MainState)  # Line ~65
    child_state.tool_filter = tools                        # Line ~66
    child_state.memory_slice = {}                          # Line ~67
    result = await asyncio.wait_for(
        run_agent_loop(child_state, task), timeout=timeout  # Line ~69
    )
    return result["summary"]                                 # Line ~71

# Line ~65 : new_clone copies config but NOT session history. This
#            ensures the subagent does not leak private context.
# Line ~66 : tool_filter restricts which tools the subagent may call.
#            If you only pass ["web_search"], the subagent cannot
#            write files or run terminal commands.
# Line ~67 : Blank memory slice prevents the subagent from reading
#            your entire memory store.
# Line ~69 : asyncio.wait_for enforces the timeout. If the subagent
#            hangs, it raises asyncio.TimeoutError and returns a
#            partial summary.
```

**Master Prompt for This Chapter:**

```
You are continuing my Hermes Agent deep-dive education from Chapter 5.
Explain the automation stack architecture:
1. How does skill trigger matching work and why is YAML frontmatter
   parsed before markdown body?
2. What prevents a subagent from accessing the parent session's
   private memories? Trace the isolation mechanism.
3. Why does install_plugin use asyncio.to_thread for download?
4. How does Hermes identify its own crontab entries on macOS?
5. Which badges are incremented by skill creation, plugin install,
   cron add, delegate_task, and background process execution?
Conclude with exactly 5 questions to test my understanding.
```

**Chapter Conclusion — What You Have Learned**

1. Skills are just Markdown with YAML. The agent parses triggers at load time and matches against lowercase user input. There is no magic — just fast string matching.
2. Subagent isolation is a hard boundary: `new_clone()` copies config, not context. This is why you can safely delegate untrusted tasks.
3. `asyncio.to_thread()` is the secret sauce that keeps your 2015 MacBook responsive during network downloads and heavy operations.
4. Cron jobs are plain macOS crontab entries with Hermes tags. You can read them with `crontab -l` and edit them manually if needed.
5. The automation badge suite (skillsmith, plugin_goblin, cron_necromancer, subagent_commander, background_process_enjoyer) is tracked by the same scanner engine that reads state.db incrementally.

**5 Questions to Check Your Understanding:**

1. You have 200 skills in `~/.hermes/skills/`. Why does skill matching still take <50ms on a 2015 MacBook, and what hardware factor (SSD vs HDD) makes this possible?
2. A subagent is given `tools: ["web_search", "web_extract"]`. It tries to call `write_file`. What happens and why?
3. You run `hermes plugin install heavy_computation`. The download is 500 MB. Why does your Terminal not freeze, and which Python mechanism ensures this?
4. You see this crontab line: `0 9 * * * /usr/local/bin/hermes run --skill daily_log # hermes-cron:daily_log`. If you delete the comment, what breaks in `hermes cron list`?
5. If `subagent_commander` requires 5 lifetime `delegate_task` calls, and each call forks a new `HermesState`, does the parent session's `memory_store.db` grow with each call? Explain.
