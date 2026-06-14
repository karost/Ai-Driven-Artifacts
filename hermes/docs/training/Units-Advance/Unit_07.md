# Unit 7: Session Quality — Lifestyle Patterns, Vibe Coding, and Marathon Endurance

## Lab 7: Unlocking Weekend Warrior, Night Owl, Early Bird Cron, Supposed to Be Quick, One More Small Change, Vibe Architect, and Marathon Runner
Level: Intermediate
Estimated Time: ~90 minutes
Prerequisites: Hermes Agent v0.15.1 installed, dashboard running at `http://127.0.0.1:9119`, at least 10 prior sessions in `~/.hermes/state.db`, and a 2015 MacBook Pro ready for extended thermal loads.

### Lab Objectives

By the end of this lab you will be able to:

1. Query your session-quality badge progress via the Achievements API.
2. Design a weekend session strategy to advance **Weekend Warrior**.
3. Execute a late-night spiral that unlocks **Night Owl** and **This Was Supposed To Be Quick**.
4. Schedule a morning cron job that contributes to **Early Bird Cron**.
5. Drive a refactoring loop that advances **One More Small Change** and **Vibe Architect**.
6. Sustain an active session long enough to make progress on **Marathon Runner**.
7. Interpret the difference between `lifetime` and `best_session` tracking kinds.

### Why This Lab Matters

Session-quality badges measure *when*, *how long*, and *how deep* you work — not just the raw volume of commands. On a 2015 MacBook Pro, long sessions teach real hardware discipline: thermal throttling after 90 minutes, battery sag below 20 %, and the fan curve that tells you it is time to save a checkpoint. These badges turn your machine's limitations into a meta-game. Understanding them means understanding your own cadence as an operator.

### Step-by-Step Instructions

#### Step 1: Inspect Current Progress (5 minutes)

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | select(.id | IN("weekend_warrior","night_owl","early_bird_cron","supposed_to_be_quick","one_more_small_change","vibe_architect","marathon_runner")) | {id, tier, progress, thresholds}'
```

Note the current tier and progress for each target badge. If the API is offline, open `hermes dashboard` → Achievements tab.

#### Step 2: Weekend Warrior — Run a Saturday Deep Session (15 minutes)

Open Hermes on a Saturday or Sunday. Run:

```bash
hermes --tui
```

Inside the session, perform at least 50 tool calls (file edits, web searches, terminal commands). Then save:

```
/save
```

Exit. The session is flagged as a weekend session. Thresholds: **Copper 10**, Silver 30, Gold 80, Diamond 200, Olympian 500. Weekend sessions are `lifetime` cumulative.

#### Step 3: Night Owl — Stay Active After 22:00 (15 minutes)

Start a session between 22:00 and 05:00 local time. On your MacBook:

```bash
hermes --tui
```

Run a task that naturally extends: refactoring a Python module, scraping a site, or writing a skill. Use at least 30 tool calls before saving. Thresholds: **Copper 20**, Silver 60, Gold 150, Diamond 400, Olympian 1,000. These are also `lifetime` cumulative.

#### Step 4: Early Bird Cron — Schedule a 06:00 Job (10 minutes)

```bash
hermes cron add "early bird status check" --schedule "0 6 * * *"
```

Action payload:

```
At 6 AM every day:
1. Run `uptime` and `df -h` via terminal.
2. Save the output to ~/macbook-dailies/$(date +%F).md.
```

Test it once manually:

```bash
hermes cron run "early bird status check"
```

Thresholds: **Copper 5**, Silver 15, Gold 40, Diamond 100, Olympian 250. Only cron jobs firing between 05:00–09:00 count.

#### Step 5: Supposed To Be Quick — Let a Task Spiral (20 minutes)

Start a session with a "small" request:

```
Just fix this one CSS spacing issue.
```

Then keep asking follow-ups: test it, tweak it, test again, add a breakpoint, check logs, refactor the component. Do not batch your requests — send each as a separate message. Aim for 60+ messages in one session. Thresholds: **Copper 300**, Silver 600, Gold 1,200, Diamond 2,500, Olympian 6,000. This is a `best_session` peak — only your highest count ever matters.

#### Step 6: One More Small Change + Vibe Architect — File Iteration Gauntlet (20 minutes)

In the same session (or a new one), repeatedly edit the same file:

```
Patch style.css, then test, then patch again.
```

Each `patch` or `write_file` call counts as a file tool call. Aim for 50+ file tool calls. Separately, create or touch 20+ distinct files (temp configs, stubs, logs). Thresholds:
- **One More Small Change:** Copper 150, Silver 400, Gold 1,000, Diamond 3,000, Olympian 8,000 (`best_session`).
- **Vibe Architect:** Copper 300, Silver 700, Gold 1,500, Diamond 4,000, Olympian 10,000 (`best_session`).

Save and exit.

#### Step 7: Marathon Runner — Keep the Session Alive (5 minutes)

`best_session` duration is measured in minutes. To make progress, the session must remain active without long idle gaps. On a 2015 MacBook Pro, keep the terminal window open and send a message every few minutes. Thresholds: **Copper 60**, Silver 180, Gold 480, Diamond 1,200, Olympian 3,000 minutes. For this lab, reaching Copper (1 hour) in a single contiguous session is sufficient.

#### Step 8: Verify Unlocks and Rescan (5 minutes)

```bash
curl -X POST http://127.0.0.1:9119/api/plugins/hermes-achievements/rescan
```

Re-run the Step 1 query and confirm progress bars moved.

### Troubleshooting

- **Badges not updating after a session:** The scan engine caches snapshots. Force a rescan with the POST command above. First-time scans are background and non-blocking.
- **MacBook sleeps mid-session:** macOS sleep pauses the process timer. Disable sleep temporarily with `caffeinate -d` in a second Terminal tab.
- **Cron job not counted for Early Bird:** Verify the system timezone matches the cron schedule. Check with `date` and `hermes cron list`.
- **Vibe Architect not advancing:** Only `write_file`, `patch`, and sometimes `terminal` file redirects count. Verify via dashboard detail view.

### Expected Outcome

- Weekend Warrior progress moves from current → current + 1 (or unlocks Copper if this was your 10th weekend session).
- Night Owl and/or Early Bird Cron show visible progress in the dashboard.
- At least one `best_session` badge (Supposed To Be Quick, One More Small Change, Vibe Architect, or Marathon Runner) shows a new personal best.
- You understand that `lifetime` badges reward persistence while `best_session` badges reward peak performance.

### Lab 7 Use Case Completed

You now track your own coding lifestyle through Hermes. You know whether you are a weekend sprinter, a midnight debugger, or a morning cron architect. Your 2015 MacBook has survived the gauntlet — and you have the progress bars to prove it.

### Training Idea / Self-Improvement Focus

Session quality data is feedback about *you*, not just the machine. If Night Owl is your highest badge, consider whether late-night work is sustainable. If Marathon Runner spikes past Gold, ask whether those 8-hour sessions were productive or just hard to kill. Use the badge data to calibrate your schedule. On limited hardware, intentional pacing beats brute-force endurance.

### Challenge (Recommended)

1. Within the next 30 days, aim for **Gold tier** on one `best_session` badge.
2. Keep a Markdown journal at `~/session-quality-log.md`. After each long session, record: date, duration, peak message count, and whether the MacBook thermal-throttled.
3. At the end of 30 days, analyze the log. Do your highest-badge days correlate with better outputs or just longer inputs?

### Emotional Reward

**You have turned your calendar and your stamina into a scoreboard. That is not vanity — it is telemetry. Outstanding work!**

---

## Chapter 7: How Session Quality Is Measured Inside the Scanning Engine

**Top Ideal Study Objectives:**
- Trace how `state.db` session timestamps are bucketed into weekend, night, and morning categories.
- Understand the difference between `lifetime` accumulation and `best_session` peak detection.
- Connect the scanning engine's incremental cache to the dashboard progress bars you observed in Lab 7.

**Description:**
This chapter examines the backend logic that converts raw session history into the seven Session Quality badges. When the cron job fired at 6 AM in Lab 7, the scanner did not just increment a counter — it parsed the session's ISO timestamp, extracted the weekday and hour, and routed the increment to the correct `lifetime` bucket. For your 60-message spiral session, it compared the new peak to the previous best and atomically updated `best_session` if the new value was higher. On a 2015 MacBook with a spinning disk or old SSD, this scan is cached so that repeated dashboard visits feel instant.

**Actions List (Topics):**
1. Locate the timestamp parser in the achievements plugin source.
2. Identify the `best_session` comparison logic and its atomic update path.
3. Trace how weekend/night/morning hour filtering is implemented.
4. Observe how the snapshot cache (`SNAPSHOT_TTL_SECONDS = 120`) avoids re-parsing unchanged sessions.

**Full Source Code Snippets with Line-by-Line Explanations:**

```python
# hermes-achievements plugin: scan_engine.py (conceptual reconstruction)

class SessionQualityScanner:
    def __init__(self, state_db_path: str, user_state: dict):
        self.db = state_db_path
        self.state = user_state                    # state.json in memory
        self.THRESHOLDS = {
            "weekend_warrior":   [10, 30, 80, 200, 500],
            "night_owl":         [20, 60, 150, 400, 1000],
            "early_bird_cron":   [5, 15, 40, 100, 250],
            "supposed_to_be_quick": [300, 600, 1200, 2500, 6000],
            "one_more_small_change": [150, 400, 1000, 3000, 8000],
            "vibe_architect":    [300, 700, 1500, 4000, 10000],
            "marathon_runner":   [60, 180, 480, 1200, 3000],
        }

    def scan_session(self, session: dict) -> dict:
        """
        session: {
          "id": "uuid",
          "started_at": "2026-06-06T23:15:00Z",
          "ended_at": "2026-06-07T01:45:00Z",
          "message_count": 340,
          "file_tool_calls": 180,
          "files_touched": 420,
          "source": "cli"
        }
        """
        dt = datetime.fromisoformat(session["started_at"].replace("Z", "+00:00"))
        duration_min = self._duration(session)

        # --- Lifetime bucketing by timestamp ---
        if dt.weekday() >= 5:                        # Line ~45
            self.state["weekend_warrior"] += 1       # Line ~46

        if 22 <= dt.hour or dt.hour < 5:             # Line ~49
            self.state["night_owl"] += 1             # Line ~50

        # Note: early_bird_cron is handled by the cron dispatcher,
        # not the session scanner, because it tracks cron executions.

        # --- Best-session peak detection ---
        self._maybe_update_best("supposed_to_be_quick", session["message_count"])   # Line ~57
        self._maybe_update_best("one_more_small_change", session["file_tool_calls"]) # Line ~58
        self._maybe_update_best("vibe_architect", session["files_touched"])          # Line ~59
        self._maybe_update_best("marathon_runner", duration_min)                     # Line ~60

        return self.state

    def _maybe_update_best(self, badge_id: str, new_value: int):
        """
        Atomic peak update. Only replaces the stored best if new_value is strictly greater.
        This is a single dict assignment — thread-safe because Hermes is single-process
        and the GIL protects the dict mutation.
        """
        old_best = self.state.get(f"{badge_id}_best", 0)   # Line ~70
        if new_value > old_best:                             # Line ~71
            self.state[f"{badge_id}_best"] = new_value       # Line ~72
            print(f"New best for {badge_id}: {new_value}")   # Line ~73

    def _duration(self, session: dict) -> int:
        start = datetime.fromisoformat(session["started_at"].replace("Z", "+00:00"))
        end   = datetime.fromisoformat(session["ended_at"].replace("Z", "+00:00"))
        return int((end - start).total_seconds() // 60)      # Line ~79

# Line-by-line:
# Line 45-46 : Weekend detection uses Python's datetime.weekday().
#              Monday=0 ... Saturday=5, Sunday=6. Sessions starting on
#              Saturday or Sunday increment Weekend Warrior.
#
# Line 49-50 : Night Owl uses hour-of-day filtering. 22:00 to 04:59 inclusive.
#              A session starting at 23:15 counts. A session starting at 05:00
#              does not. This is a simple integer range check — fast on old
#              hardware because it never touches the session body.
#
# Line 57-60 : Peak detection runs for every session. Even if you had a quiet
#              10-message session, the scanner still checks. The dict lookup is
#              O(1) and the comparison is a single CPU instruction. On a 2015
#              MacBook, scanning 1,000 sessions takes < 100 ms after caching.
#
# Line 70-73 : The old best is read, compared, and overwritten only if the
#              new value is strictly greater. This prevents regressions.
#              The print line becomes a dashboard event in production.
#
# Line 79    : Duration is integer minutes, truncated. A session of 59 minutes
#              and 59 seconds contributes 59, not 60, to Marathon Runner.
```

**Master Prompt for This Chapter:**

```
You are continuing my Hermes Agent deep-dive education from Chapter 7.
Explain the Session Quality scanning engine:
- How does the scanner distinguish a weekend session from a weekday session
  using only the started_at timestamp (Line 45)?
- Why is Night Owl defined as 22:00-05:00 instead of a simpler "after midnight" rule?
- What is the computational cost of _maybe_update_best() on a 2015 MacBook Pro
  with 1,000 historical sessions?
- If I run two sessions on the same Saturday, how many times does
  Weekend Warrior increment? What kind metric drives this?
- Marathon Runner uses duration_min. If my session starts at 23:50 and ends at
  00:40 the next day, what value is recorded and why?
- Why does Early Bird Cron track cron job executions rather than regular session
  starts, and where is that counted instead?
Use a 2015 MacBook Pro as the hardware context.
Conclude with exactly 5 questions to test my understanding.
```

**Chapter Conclusion — What You Have Learned**

1. `lifetime` badges count events cumulatively. Weekend Warrior and Night Owl never reset; every qualifying session adds +1.
2. `best_session` badges store a single peak. If you hit 340 messages once, that number persists until you beat it.
3. Timestamp parsing is lightweight. The scanner only reads the session header (started_at, ended_at) for quality badges, not the full message log.
4. Atomic comparison protects progress. The `>` check in `_maybe_update_best` guarantees that a bad session cannot lower your badge.
5. Caching makes repeated dashboard visits instant. After the first scan, `SNAPSHOT_TTL_SECONDS = 120` reuses the payload without re-parsing state.db.

**5 Questions to Check Your Understanding:**

1. You start a session on Friday at 21:00 and finish at 23:30. Which `lifetime` badge increments, if any? Explain using Line 45 and Line 49.
2. If your current best for `supposed_to_be_quick` is 620 (Silver tier) and today's session reaches 1,100 messages, what tier do you unlock? Which line in the scanner makes this decision?
3. Why is `_maybe_update_best` considered atomic in the Hermes single-process model, and what would change if Hermes moved to a multi-process architecture?
4. A cron job is scheduled for 08:30 every day. Does it count toward Early Bird Cron? Why or why not?
5. Your 2015 MacBook takes 2.3 seconds to scan `state.db` the first time, but 80 ms on subsequent visits. Which caching mechanism is responsible, and what is the TTL?
