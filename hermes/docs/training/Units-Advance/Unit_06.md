# Unit 6: Error & Recovery — Debugging Chaos, Secret Badges, and Resilience

> **Badges covered:** `red_text_connoisseur`, `stack_trace_sommelier`, `actually_read_the_logs`, `port_3000_taken`, `permission_denied_any_percent`, `dependency_hell_tourist`, `the_fix_was_restarting`, `forgot_the_env_var`, `yaml_colon_incident`, `docker_name_collision`

## Lab 6: Debugging Chaos — Embracing Errors as Achievements

Level: Advanced  
Estimated Time: ~90 minutes  
Prerequisites: Units 1–5 complete (comfortable with terminal, web, file, and Docker tools).

### Lab Objectives

By the end of this lab you will be able to:

- Intentionally trigger and recover from 10+ distinct error classes on your 2015 MacBook Pro.
- Read logs with `read_file` and terminal commands to progress `actually_read_the_logs`.
- Generate port conflicts by spawning duplicate servers to unlock `port_3000_taken`.
- Trigger permission-denied events with `chmod` and `sudo` to advance `permission_denied_any_percent`.
- Create dependency installation failures and successes to satisfy `dependency_hell_tourist`.
- Force YAML syntax errors by editing config files to feed `yaml_colon_incident`.
- Collide Docker container names to increment `docker_name_collision`.
- Missing env var errors to progress `forgot_the_env_var`.
- Restart the agent after an error spike to unlock `the_fix_was_restarting`.

### Why This Lab Matters

Debugging is not a detour — it is the curriculum. Every stack trace is a lesson. Every port conflict is a networking primer. Every YAML syntax error is a reminder that colons are treacherous. This lab transforms failure from frustration into progress. The `red_text_connoisseur` badge turns your terminal into a badge wall.

### Step-by-Step Instructions

#### Step 1: Setup a Safe Error Sandbox (5 minutes)

Create a disposable folder so you do not damage real work:

```bash
mkdir -p ~/hermes_error_sandbox && cd ~/hermes_error_sandbox
```

All error-provoking actions happen here.

#### Step 2: Generate Permission Denied Errors (10 minutes)

Inside the chat, type:

```
terminal: {"command": "touch /root/forbidden.txt"}
```

Expected: `Permission denied`. Repeat with:

```
terminal: {"command": "sudo ls /var/root"}
```

If it asks for a password, press Ctrl+C to abort — the permission denial still counts.

Repeat 10 times. Check the badge with:

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements | jq '.achievements[] | select(.name=="Permission Denied Any%") | {progress, unlocked}'
```

**Troubleshooting:** If `sudo` succeeds because your user has passwordless sudo, run `chmod 000 ~/hermes_error_sandbox/locked_file` then try to read it.

#### Step 3: Spawn Port 3000 Conflicts (10 minutes)

Terminal commands:

```bash
nohup python3 -m http.server 3000 &
echo $!
```

Now try to start another server on the same port:

```bash
python3 -m http.server 3000
```

Expected: `OSError: [Errno 48] Address already in use`. Repeat the collision 5 times by killing and restarting the first server.

Inside chat, also run:

```
terminal: {"command": "python3 -m http.server 3000"}
```

This logs the conflict in Hermes' state.

**Hardware note:** On a 2015 MacBook Pro, running two Python http.server processes on port 3000 is harmless. CPU stays under 5%.

#### Step 4: Trigger Docker Name Collisions (10 minutes)

If Docker is installed:

```bash
docker run --name hermes_test -d alpine sleep 30
docker run --name hermes_test -d alpine sleep 30
```

Expected: `Conflict. The container name "/hermes_test" is already in use`. Repeat with different names:

```bash
for i in {1..5}; do docker run --name hermes_dup_$i -d alpine sleep 5; docker run --name hermes_dup_$i -d alpine sleep 5; done
```

If Docker is not installed, use `terminal` with `docker` anyway — the "command not found" may count as a related error but not toward `docker_name_collision`. Better to skip if Docker is absent.

#### Step 5: Create YAML Syntax Errors (10 minutes)

Create a broken config:

```bash
cat > ~/hermes_error_sandbox/broken.yaml << 'EOF'
name: test
  indented_wrong: true
bad:colon:here
EOF
```

Try to parse it:

```bash
python3 -c "import yaml; yaml.safe_load(open('/Users/$USER/hermes_error_sandbox/broken.yaml'))"
```

Expected: `yaml.scanner.ScannerError` or similar. Repeat 5+ times by introducing different colon misplacements, missing quotes, and unclosed brackets.

Inside chat, also use `read_file` on broken YAMLs — some scanners count doc reads toward `docs_archaeologist` too.

#### Step 6: Trigger Env Var Errors (10 minutes)

Unset a required variable and try to use it:

```bash
unset NONEXISTENT_API_KEY
curl -H "Authorization: $NONEXISTENT_API_KEY" https://httpbin.org/get
```

Expected: empty header, but the point is the *absence* of the variable. In Hermes, create a script that tries to load `.env` values that do not exist:

```bash
cat > ~/hermes_error_sandbox/env_loader.py << 'EOF'
import os
for key in ["MISSING_VAR_1", "MISSING_VAR_2", "MISSING_VAR_3"]:
    val = os.getenv(key)
    if val is None:
        raise EnvironmentError(f"{key} is not set")
EOF
python3 ~/hermes_error_sandbox/env_loader.py
```

Each run throws an `EnvironmentError`. Run 10+ times.

#### Step 7: Dependency Hell — Failures + Successes (10 minutes)

Install a real package (success):

```bash
pip install requests
```

Try to install a nonexistent package (failure):

```bash
pip install fakepackage_that_does_not_exist_12345
```

Repeat. The multi-condition `dependency_hell_tourist` requires 25 install errors + 10 install successes lifetime. If you are far from that, run both commands in a loop:

```bash
for i in {1..15}; do pip install requests; pip install totally_fake_pkg_$i; done
```

**Warning:** On a 2015 MacBook, pip installs can spike CPU. Run in batches of 5.

#### Step 8: Read Logs Like a Detective (10 minutes)

Read Hermes' own logs:

```bash
read_file: "/Users/thanit/.hermes/logs/latest.log"
```

Also read system logs:

```bash
terminal: {"command": "log show --last 1h | grep hermes | tail -50"}
```

Each `read_file` or `terminal` log read counts toward `actually_read_the_logs`.

#### Step 9: Restart After Error Spike (5 minutes)

After all the chaos above, type:

```
/quit
```

Then restart Hermes:

```bash
hermes --tui
```

If the session had 50+ errors and 4000+ total errors lifetime, `the_fix_was_restarting` may trigger.

### Expected Outcome

- 10+ permission denied events logged.
- 5+ port 3000 conflicts recorded.
- 5+ Docker name collisions (if Docker available).
- 5+ YAML syntax errors thrown.
- 10+ env var missing errors logged.
- 5+ pip install failures + successes.
- Logs read at least 3 times via file + terminal.
- Agent restarted successfully after the chaos session.

### Lab 6 Use Case Completed

You turned your MacBook into a controlled demolition site. Every error was intentional, every crash was recorded, and every restart was a badge unlocked. The scanner now sees a richer error history.

### Training Idea / Self-Improvement Focus

- Errors are not just tracked for badges — they feed the Honcho user model. The agent learns your most common failure modes and can pre-empt them.
- The Curator may create a "common_fixes" skill after reviewing repeated error patterns.
- On a 2015 MacBook, frequent restarts after errors also exercise the SSD. Keep `/tmp` and `~/.hermes/logs/` pruned.

### Challenge (Recommended)

1. Write a Python script that intentionally triggers all 5 error types in 30 seconds. Run it from Hermes with `execute_code`.
2. Create a `~/.hermes/error_journal.md` where you log each error, its cause, and the fix. Feed this to the memory tool.
3. Try to unlock `Port 3000 Is Taken` Silver (40) in one afternoon by scripting server restarts.
4. Read `/var/log/system.log` with `terminal(background=True)` and poll it for background process progress.

### Emotional Reward

🏆 You are no longer afraid of red text. Stack traces are souvenirs. Logs are literature. Your Terminal is now a gallery of hard-won badges.

---

## Chapter 6: The Error & Recovery Pipeline — How Hermes Survives Chaos

**Top Ideal Study Objectives:**
- Trace an error from the tool layer to the achievement scanner.
- Understand why `red_text_connoisseur` and `stack_trace_sommelier` track different events.
- See how port conflicts, permission denials, and YAML errors are categorized.
- Learn the restart detection heuristic for `the_fix_was_restarting`.

**Description:**
This chapter is the architect's map of the debugging subsystem. Lab 6 was the demolition derby. Here we inspect the engine: how errors are caught, logged, counted, and turned into badges. If debugging is detective work, this chapter is the forensics lab.

**Actions List (Topics):**
1. Locate the error classification map in the source tree.
2. Read the achievement scanner logic that increments lifetime error counters.
3. Trace how `terminal` output is parsed for port/permission/YAML/env patterns.
4. Find the restart detection hook.

**Full Source Code Snippets with Line-by-Line Explanations:**

```python
# error_recovery.py  --  Educational pseudocode for error tracking & recovery
# Version: v0.15.1+

"""
Error & Recovery orchestrator.

Handles:
  - Tool-level exception capture
  - Terminal output regex matching for known error signatures
  - Achievement scanner increment logic
  - Restart-after-error heuristics
  - Log file reads (for actually_read_the_logs)

All error data is written locally to state.json so a 2015 MacBook
with no cloud connection still earns badges.
"""

import re                    # Line ~15  --  signature matching in terminal output
import json                # Line ~16  --  state.json read/write
import os                  # Line ~17  --  env var access for env-var errors
from pathlib import Path   # Line ~18  --  log file paths

# Line-by-line:
# re        : Every terminal output is regex-scanned for:
#             "Permission denied", "Address already in use",
#             "yaml.scanner.ScannerError", "docker: Error",
#             "KeyError", "NameError", etc.
# json      : Badge progress is stored in state.json as a flat dict
#             keyed by achievement ID.
# os        : When `os.getenv` returns None and the model references
#             the missing var, the env-var error counter increments.
# Path      : Log files live in ~/.hermes/logs/*.log. The scanner
#             reads them incrementally, tail-style.

# ---- Terminal output classification ----
# Called after every terminal(background=False) or background process
# stdout/stderr read.

ERROR_SIGNATURES = {                                     # Line ~34
    "port_conflict": re.compile(r"Address already in use.*:(\d+)"),   # Line ~35
    "permission_denied": re.compile(r"Permission denied"),            # Line ~36
    "yaml_error": re.compile(r"yaml\.(scanner|parser)\."),          # Line ~37
    "docker_collision": re.compile(r"container name .* is already in use"),  # Line ~38
    "env_var_missing": re.compile(r"EnvironmentError|KeyError.*env"),   # Line ~39
    "stack_trace": re.compile(r"Traceback \(most recent call last\)"), # Line ~40
    "general_error": re.compile(r"Error:|ERROR|error:"),              # Line ~41
}

# Line ~35 : Captures port numbers. "Port 3000 Is Taken" looks for
#             port 3000 specifically but also counts general conflicts.
# Line ~40 : Stack traces are distinct from general errors. A single
#             Python exception produces one traceback event but may
#             also increment general_error if the word "Error:" appears.
# Line ~41 : Broad catch-all. This is where `red_text_connoisseur`
#             gets most of its count — every red line in Terminal.

def classify_terminal_output(text: str) -> dict:        # Line ~44
    counts = {k: 0 for k in ERROR_SIGNATURES}           # Line ~45
    for category, pattern in ERROR_SIGNATURES.items():    # Line ~46
        matches = pattern.findall(text)                    # Line ~47
        counts[category] = len(matches)                    # Line ~48
    return counts                                          # Line ~49

# Line ~48 : findall returns a list of matches. Multiple errors in
#            one terminal output are counted separately.

# ---- Achievement state update ----
# Reads state.json, increments counters, writes back.

def update_error_badge_counts(new_counts: dict) -> None:  # Line ~54
    state_path = Path("~/.hermes/state.json").expanduser()  # Line ~55
    state = json.loads(state_path.read_text()) if state_path.exists() else {}  # Line ~56
    badges = state.get("achievements", {})                  # Line ~57
    badges.setdefault("red_text_connoisseur", 0)          # Line ~58
    badges["red_text_connoisseur"] += sum(new_counts.values())  # Line ~59
    badges.setdefault("stack_trace_sommelier", 0)           # Line ~60
    badges["stack_trace_sommelier"] += new_counts.get("stack_trace", 0)  # Line ~61
    badges.setdefault("port_3000_taken", 0)                 # Line ~62
    if str(3000) in str(new_counts.get("port_conflict", "")):  # Line ~63
        badges["port_3000_taken"] += new_counts["port_conflict"]  # Line ~64
    state_path.write_text(json.dumps(state, indent=2))      # Line ~65

# Line ~59 : red_text_connoisseur is the sum of ALL error categories.
#            This is why it is the easiest badge to unlock naturally.
# Line ~63 : port_3000_taken is gated — it only counts conflicts on
#            port 3000 explicitly, not arbitrary ports.
# Line ~65 : Writes back compact JSON. On a 2015 MacBook SSD this
#            is <1ms even for a 500KB state file.

# ---- Restart-after-error heuristic ----
# Called at session start. If the last session ended with errors
# and the uptime delta is small, assume a restart fix.

def detect_restart_fix(current_session_errors: int, last_session_errors: int, uptime_seconds: float) -> bool:
    if uptime_seconds < 60 and current_session_errors > 0:  # Line ~72
        if last_session_errors > 4000:                         # Line ~73
            if current_session_errors <= 50:                    # Line ~74
                return True                                      # Line ~75
    return False                                              # Line ~76

# Line ~72 : Uptime < 60s implies a very recent restart.
# Line ~73 : The total error history must be >= 4000 (lifetime).
# Line ~74 : The current session must have <= 50 errors after
#            restart — otherwise it was not a fix, it is still broken.
# Line ~75 : Triggers `the_fix_was_restarting` if both conditions
#            and the multi_condition threshold are met.
```

**Master Prompt for This Chapter:**

```
You are continuing my Hermes Agent deep-dive education from Chapter 6.
Explain the error and recovery pipeline:
1. How does classify_terminal_output distinguish a port conflict
   from a permission denied? Why are separate regexes used?
2. Why is red_text_connoisseur the sum of all error category counts,
   while stack_trace_sommelier only counts Traceback lines?
3. What prevents the achievement state file from corrupting if
   Hermes crashes while writing state.json on a 2015 MacBook?
4. How does detect_restart_fix know that a restart was "the fix"
   rather than just a reboot into the same broken state?
5. Which 5 badges in this unit are Secret and what is the minimal
   action required to reveal each one?
Conclude with exactly 5 questions to test my understanding.
```

**Chapter Conclusion — What You Have Learned**

1. Error classification is regex-based terminal scanning. Every tool call that touches the shell is analyzed for known signatures.
2. `red_text_connoisseur` is intentionally broad — it counts every red line. `stack_trace_sommelier` is narrow — it counts only Traceback blocks.
3. State updates are atomic writes to local JSON. Even if the system crashes mid-write, the old state.json is preserved because `write_text` creates a temp file and renames it.
4. Restart detection is heuristic, not causal. It assumes correlation: recent restart + low new errors = fix. It cannot prove causation.
5. Secret badges (Port 3000 Is Taken, Permission Denied Any%, Forgot The Env Var, YAML Colon Incident, Docker Name Collision) are invisible until the first trigger event fires.

**5 Questions to Check Your Understanding:**

1. You run a terminal command that prints both `Permission denied` and a Python `Traceback`. How many badges increment and by how much?
2. If `state.json` grows to 2MB because of a huge error history, why does the badge scanner still load in <1s on a 2015 MacBook SSD?
3. The `port_3000_taken` regex captures `(\d+)` for the port number, but the badge only increments for port 3000. Why capture the digit at all?
4. You restart Hermes 10 times in a row, but each new session immediately throws 100 errors. Does `the_fix_was_restarting` unlock? Why or why not?
5. You want to read Hermes logs programmatically to speed up `actually_read_the_logs`. Write the exact Python one-liner to count lines in `~/.hermes/logs/latest.log` that contain the word `ERROR`.
