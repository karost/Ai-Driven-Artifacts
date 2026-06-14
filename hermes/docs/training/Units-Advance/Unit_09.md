# Unit 9: Secret Achievements — The Hidden Badges of Hermes

## Lab 9: Unlocking Port 3000 Taken, Permission Denied Any%, Forgot the Env Var, YAML Colon Incident, Docker Name Collision, Rollback Wizard, One Character Fix, and Legend
Level: Advanced
Estimated Time: ~120 minutes
Prerequisites: Hermes Agent v0.15.1, dashboard accessible, terminal and Docker (optional) available, and permission to trigger intentional errors on a 2015 MacBook Pro without breaking production systems.

### Lab Objectives

By the end of this lab you will be able to:

1. Trigger each of the 7 non-Legend secret achievements in a controlled way.
2. Distinguish secret `lifetime` badges from secret `multi_condition` badges.
3. Use the `/rollback` command correctly to advance **Rollback Wizard**.
4. Craft a single-character patch that satisfies the **One Character Fix** multi-condition.
5. Interpret the hidden-until-triggered state of secret badges in the dashboard.
6. Explain why **Legend** is the ultimate endgame badge and outline a realistic path to it.
7. Force a full rescan and verify secret badge discovery in `state.json`.

### Why This Lab Matters

Secret achievements are invisible until your behavior triggers the first signal. They document the "scars" of real engineering: port conflicts, permission failures, missing env vars, YAML typos, Docker collisions, panic rollbacks, and microscopic bug fixes. These are not participation trophies — they are forensic evidence that you have fought real systems and won (or at least survived). On a 2015 MacBook Pro with 16 GB RAM, you will hit these errors *naturally* because older hardware has tighter resource constraints. This lab teaches you to trigger them intentionally so you can recognize them when they happen for real.

### Step-by-Step Instructions

#### Step 1: Verify Secret Badge States (5 minutes)

Secret badges are invisible in the dashboard until unlocked. Confirm via API:

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | select(.id | IN("port_3000_taken","permission_denied_any_percent","forgot_the_env_var","yaml_colon_incident","docker_name_collision","rollback_wizard","one_character_fix","legend")) | {id, visible, tier, progress}'
```

Initially, `visible` should be `false` and `tier` should be `null` for most. If you have already triggered one, it will show `visible: true`.

#### Step 2: Port 3000 Is Taken — Trigger a Port Conflict (10 minutes)

Start a server on port 3000 in one Terminal tab:

```bash
python3 -m http.server 3000
```

In a second tab, inside a Hermes session, try to start another server:

```bash
hermes --tui
```

Then ask:

```
Run a Python HTTP server on port 3000 using terminal.
```

The agent executes:

```bash
python3 -m http.server 3000
```

It fails with:

```
OSError: [Errno 48] Address already in use
```

This error is logged. The achievements scanner counts it toward **Port 3000 Is Taken**.

Thresholds: **Copper 15**, Silver 40, Gold 100, Diamond 300, Olympian 1,000 (`lifetime`).

Kill the first server (Ctrl+C) before proceeding.

#### Step 3: Permission Denied Any% — Trigger a `sudo` or File-System Failure (10 minutes)

In a Hermes session, ask:

```
Read the file /root/secret.txt
```

The agent attempts:

```bash
cat /root/secret.txt
```

It fails with:

```
cat: /root/secret.txt: Permission denied
```

Alternatively, run a Docker command without `sudo` on a Docker socket:

```
Run: docker run --rm hello-world
```

If Docker requires root, the error is logged as "permission denied."

Thresholds: **Copper 25**, Silver 75, Gold 200, Diamond 600, Olympian 1,500 (`lifetime`).

#### Step 4: Forgot The Env Var — Simulate a Missing Environment Variable (10 minutes)

Create a script that expects a variable:

```bash
cat > ~/env_test.py << 'EOF'
import os
api_key = os.environ["MY_API_KEY"]
print(f"Key is {api_key}")
EOF
```

In a Hermes session, run it without setting the variable:

```
Execute the Python script at ~/env_test.py
```

The agent runs:

```bash
python3 ~/env_test.py
```

It fails with:

```
KeyError: 'MY_API_KEY'
```

This is an env-var error. Each instance counts toward **Forgot The Env Var**.

Thresholds: **Copper 5,000**, Silver 15,000, Gold 40,000, Diamond 100,000, Olympian 250,000 (`lifetime`).

#### Step 5: YAML Colon Incident — Introduce a Syntax Error (10 minutes)

Create a malformed YAML file:

```bash
cat > ~/broken.yaml << 'EOF'
server:
  host: localhost
  port: 3000
  debug: true
name: Test Config
EOF
```

That file is actually valid. Now introduce a colon-without-space error:

```bash
cat > ~/broken.yaml << 'EOF'
server:
  host: localhost
  port:3000
  debug: true
EOF
```

In a Hermes session, ask the agent to parse it:

```
Parse the YAML file at ~/broken.yaml using Python and print the port.
```

The agent will run:

```python
import yaml
with open("/Users/thanit/broken.yaml") as f:
    data = yaml.safe_load(f)
    print(data["server"]["port"])
```

It fails with a YAML scanner error. This counts toward **YAML Colon Incident**.

Thresholds: **Copper 1,000**, Silver 3,000, Gold 8,000, Diamond 20,000, Olympian 50,000 (`lifetime`).

#### Step 6: Docker Name Collision — Run a Container Twice (10 minutes)

If Docker is installed:

```bash
docker run -d --name test_hermes httpd:alpine
```

Then in a Hermes session:

```
Run a Docker container named test_hermes using the httpd:alpine image.
```

The agent executes:

```bash
docker run -d --name test_hermes httpd:alpine
```

It fails with:

```
docker: Error response from daemon: Conflict. The container name "/test_hermes" is already in use.
```

This counts. Clean up:

```bash
docker rm -f test_hermes
```

Thresholds: **Copper 75**, Silver 200, Gold 600, Diamond 1,500, Olympian 4,000 (`lifetime`).

If Docker is unavailable, skip and note that this badge requires Docker workflows.

#### Step 7: Rollback Wizard — Use `/rollback` After an Error (10 minutes)

In a Hermes session, make a destructive edit:

```
Write "DESTROYED" to ~/rollback_test.txt
```

The agent overwrites the file. Now realize the mistake and execute:

```
/rollback
```

The agent restores the previous state. Each `/rollback` call increments the **Rollback Wizard** counter.

Thresholds: **Copper 500**, Silver 1,500, Gold 4,000, Diamond 10,000, Olympian 25,000 (`lifetime`).

#### Step 8: One Character Fix — Patch After an Error (15 minutes)

This is a `multi_condition` secret badge. Requirements (from the catalog):
- Make a tiny single-character patch.
- It must occur after at least 5 errors in the session.
- Your total lifetime errors across all sessions must be at least 4,000.

In a Hermes session, first generate 5 trivial errors (e.g., run missing files). Then create a file with a one-character bug:

```bash
cat > ~/one_char.py << 'EOF'
def greet(name):
    return "Hello, " + name + "!"

print(greet("world")
EOF
```

Note the missing closing parenthesis on the last line. Ask the agent:

```
Run ~/one_char.py. It should fail. Then fix it with the smallest possible patch.
```

The agent identifies the missing `)` and applies:

```python
patch({
    "path": "~/one_char.py",
    "old_string": 'print(greet("world")',
    "new_string": 'print(greet("world"))'
})
```

This is a single-character addition after 5+ errors. If your lifetime error total is ≥ 4,000, the badge unlocks.

#### Step 9: Legend — Understand the Endgame (5 minutes)

**Legend** requires reaching Olympian tier in ALL other achievements. It is the ultimate `multi_condition` secret. Do not attempt to unlock it today; it is a months-long goal. Verify the conditions:

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '[.achievements[] | select(.tier != "olympian") | .id] | length'
```

If the count is 0, you have Legend. If it is 60, you have a long road ahead. Keep a checklist.

#### Step 10: Rescan and Verify (5 minutes)

```bash
curl -X POST http://127.0.0.1:9119/api/plugins/hermes-achievements/rescan
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/recent-unlocks
```

### Troubleshooting

- **Secret badges remain invisible:** They only appear after the first trigger. If you have never seen a port conflict, Permission Denied Any% stays hidden. Trigger it intentionally in this lab.
- **One Character Fix requires 4,000 lifetime errors:** If you are a new user, this badge is locked until you accumulate enough errors naturally. Use Hermes heavily on real projects.
- **Docker Name Collision requires Docker:** If Docker is not installed, this badge is unavailable. Install Docker Desktop for Mac or skip it.
- **Rollback Wizard counts `/rollback` calls:** Using `patch` to undo edits does not count. You must use the explicit `/rollback` command.
- **Legend is not a `lifetime` badge:** It is evaluated by a bulk check that iterates all achievements. Deleting `state.json` and rescanning does not help — the data comes from `state.db`.

### Expected Outcome

- At least 3 secret badges are now visible in the dashboard.
- You understand the trigger conditions for all 7 non-Legend secrets.
- One Character Fix is either unlocked (if error threshold met) or planned for future unlocking.
- You have a realistic timeline for Legend based on your current Olympian count.

### Lab 9 Use Case Completed

You have intentionally triggered the hidden badges of Hermes. These are not vanity metrics — they map to real failure modes in software engineering. The next time you see "Port 3000 is taken" at 2 AM, you will recognize it as progress toward Olympian.

### Training Idea / Self-Improvement Focus

Secret badges teach resilience. The highest-error badge (Forgot The Env Var, Olympian 250,000) is only reachable if you work at scale. Instead of fearing errors, log them. After every error, ask: "Which badge is this feeding?" On a 2015 MacBook Pro, you will generate errors faster than on modern hardware because resource limits are tighter. Turn your hardware constraints into badge acceleration.

### Challenge (Recommended)

1. In the next 14 days, aim to make **YAML Colon Incident** visible (Copper: 1,000 errors is hard to trigger intentionally, but 1 is enough for discovery).
2. Keep an "Error Log" skill:
   - Trigger: "I got an error"
   - Action: log the error type, badge it feeds, and a one-sentence fix.
3. After 14 days, review the error log. Which error type do you generate most often? That is your dominant learning vector.

### Emotional Reward

**You have looked behind the curtain. The invisible badges are the most honest ones — they reward the work no one else sees. Masterful work!**

---

## Chapter 9: How the Scanning Engine Discovers and Unlocks Secret Achievements

**Top Ideal Study Objectives:**
- Trace the visibility toggle from `visible=false` to `visible=true` on first trigger.
- Understand why secret badges use both `lifetime` and `multi_condition` tracking kinds.
- Map the scanner's error-type classification regexes to the secret badge IDs.
- Examine the Legend evaluation function and its computational cost on a 2015 MacBook Pro.

**Description:**
This chapter reveals the internal mechanics of the 8 secret achievements. Unlike visible badges, secrets start in an undiscovered state. The scanner runs a classification pass over every session's error log, tool calls, and rollback events. When a qualifying signal is detected for the first time, the badge flips from hidden to discovered. On a 2015 MacBook Pro with a SATA SSD or Fusion Drive, the full scan is the slowest operation in the achievement pipeline — which is why v0.3.0 introduced snapshot caching.

**Actions List (Topics):**
1. Locate the secret badge registry and its default visibility map.
2. Identify the error-classification regexes that detect port conflicts, permission denied, and YAML syntax errors.
3. Trace the `multi_condition` evaluator for One Character Fix and Legend.
4. Observe the snapshotted scan path that skips unchanged sessions.

**Full Source Code Snippets with Line-by-Line Explanations:**

```python
# hermes-achievements plugin: secret_scanner.py (conceptual reconstruction)

class SecretScanner:
    SECRETS = {
        "port_3000_taken":         {"kind": "lifetime",   "pattern": r"Address already in use.*:3000"},
        "permission_denied_any_percent": {"kind": "lifetime",   "pattern": r"Permission denied|operation not permitted"},
        "forgot_the_env_var":      {"kind": "lifetime",   "pattern": r"KeyError: ['\"].*['\"]|environ\[|is not set|missing env"},
        "yaml_colon_incident":     {"kind": "lifetime",   "pattern": r"yaml\.(safe_load|load|dump)|ScannerError|colon|mapping values are not allowed"},
        "docker_name_collision":   {"kind": "lifetime",   "pattern": r"Conflict\. The container name.*is already in use"},
        "rollback_wizard":         {"kind": "lifetime",   "signal":  "rollback_command_used"},
        "one_character_fix":       {"kind": "multi_condition", "conditions": {
            "tiny_patch": True, "session_errors": 5, "lifetime_errors": 4000
        }},
        "legend":                  {"kind": "multi_condition", "conditions": {
            "all_olympian": True
        }},
    }

    def __init__(self, user_state: dict):
        self.state = user_state

    def classify_error(self, error_text: str, session_stats: dict):
        """
        Called once per error in the session log.
        """
        for badge_id, meta in self.SECRETS.items():              # Line ~29
            if meta["kind"] != "lifetime":                        # Line ~30
                continue                                          # Line ~31

            pattern = meta.get("pattern")                          # Line ~34
            if pattern and re.search(pattern, error_text, re.I): # Line ~35
                self._increment_lifetime(badge_id)                # Line ~36
                self._ensure_visible(badge_id)                    # Line ~37

    def _increment_lifetime(self, badge_id: str):
        self.state.setdefault(badge_id, 0)                       # Line ~41
        self.state[badge_id] += 1                                  # Line ~42
        print(f"[Secret] {badge_id} ++ = {self.state[badge_id]}") # Line ~43

    def _ensure_visible(self, badge_id: str):
        if not self.state.get(f"{badge_id}_visible", False):      # Line ~47
            self.state[f"{badge_id}_visible"] = True              # Line ~48
            print(f"[Secret] {badge_id} DISCOVERED!")              # Line ~49

    def check_multi_condition(self, session_stats: dict, total_errors: int):
        """
        Evaluates One Character Fix and Legend after each session scan.
        """
        # --- One Character Fix ---
        ocf = self.SECRETS["one_character_fix"]                    # Line ~57
        if session_stats.get("tiny_patch", False) \                # Line ~58
           and session_stats.get("errors_in_session", 0) >= 5 \   # Line ~59
           and total_errors >= 4000:                             # Line ~60
            self._ensure_visible("one_character_fix")             # Line ~61
            # Note: OCF has no lifetime counter; it is a one-time unlock.

        # --- Legend ---
        legend = self.SECRETS["legend"]                            # Line ~65
        olympian_count = sum(                                     # Line ~66
            1 for b in self.state.get("achievements", [])         # Line ~67
            if b.get("tier") == "olympian"                       # Line ~68
        )
        total_achievements = len(self.state.get("achievements", [])) # Line ~70
        if olympian_count == total_achievements \                   # Line ~71
           and total_achievements > 0:                             # Line ~72
            self._ensure_visible("legend")                          # Line ~73
            print("[Secret] LEGEND UNLOCKED!")                    # Line ~74

# Line-by-line:
# Line 29-31 : The scanner iterates all secrets but skips multi_condition
#              entries during per-error classification. Lifetime secrets
#              are checked against every error line; multi_condition secrets
#              are evaluated once per session after stats are aggregated.
#
# Line 34-37 : Regex matching with case-insensitive flag (re.I). The pattern
#              for "port_3000_taken" specifically targets port 3000 because
#              it is the most common dev-server port. Other ports are ignored.
#              This is why the badge is called "Port 3000 Is Taken" exactly.
#
# Line 41-43 : Lifetime counters are simple integers. They grow without bound
#              until they hit the threshold. There is no ceiling; you can
#              exceed Olympian and the counter keeps climbing.
#
# Line 47-49 : Visibility flip. Once discovered, a secret badge is never
#              hidden again. Even if the counter is reset (which requires
#              POST /reset-state), the visibility bit remains unless the
#              entire state.json is wiped.
#
# Line 57-61 : One Character Fix requires a boolean flag (tiny_patch), a
#              session-local error count, and a global error count. The
#              tiny_patch flag is set by the patch tool when it detects
#              an addition or deletion of exactly 1 character.
#
# Line 65-74 : Legend iterates EVERY achievement and checks if tier equals
#              "olympian". On a 2015 MacBook Pro with 60+ achievements,
#              this is a list scan of ~60 dict lookups — negligible cost.
#              But it only runs after a full rescan, not after every session.
```

**Master Prompt for This Chapter:**

```
You are continuing my Hermes Agent deep-dive education from Chapter 9.
Explain the secret achievement discovery engine:
- When an error matches the regex in Line 35, what two side effects occur
  (Lines 36-37)? Why is the increment separate from the visibility flip?
- One Character Fix is multi_condition. Which three conditions must all be
  true (Lines 58-60), and which tool sets the tiny_patch flag?
- If I have 59 achievements at Olympian and 1 at Diamond, what does
  Line 71 evaluate to? How many more achievements must reach Olympian
  before Legend triggers?
- The re.search in Line 35 scans every error string. For a user with
  75,000 lifetime errors, how many regex matches execute during a full
  rescan? Is this a performance concern on a 2015 MacBook Pro?
- Why does the scanner skip multi_condition secrets in the per-error loop
  (Line 31), and what ensures they are still evaluated?
Use a 2015 MacBook Pro as the hardware context.
Conclude with exactly 5 questions to test my understanding.
```

**Chapter Conclusion — What You Have Learned**

1. Secret badges start invisible. The scanner flips visibility on first trigger, and the flip is permanent.
2. Lifetime secrets use regex classification. Port 3000 Is Taken is literally pinned to port 3000 — no other port counts.
3. Multi_condition secrets evaluate session aggregates. One Character Fix needs errors *and* a tiny patch in the same session.
4. Legend is a bulk Olympian check. It scans all achievements after a full rescan. The cost is negligible even on old hardware.
5. Caching v0.3.0+ means the 75,000-error regex loop only runs once. Subsequent scans skip unchanged sessions.

**5 Questions to Check Your Understanding:**

1. You trigger a port conflict on port 8080. Which line in the scanner decides whether Port 3000 Is Taken increments, and what is the result?
2. After discovering a secret badge, you delete `state.json` and force a rescan. The badge is visible again but the counter is lower. Why? Which file was the real source of truth?
3. One Character Fix requires `total_errors >= 4000`. If your lifetime error count is 3,999 and you make a tiny patch after 5 session errors, does the badge unlock? Which line is the gate?
4. Legend checks `total_achievements > 0` in Line 72. Why is this guard necessary, and what edge case does it prevent?
5. Your 2015 MacBook has 75,000 historical errors. The first full scan takes 2.3 seconds. After v0.3.0 caching, the second scan takes 80 ms. Which file stores the checkpoint that enables this speedup?
