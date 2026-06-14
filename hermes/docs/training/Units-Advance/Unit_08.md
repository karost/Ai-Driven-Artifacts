# Unit 8: Social & Community — Shared Session, Team Delegate, and Cross Platform

## Lab 8: Sharing Sessions, Delegating to Multi-User Subagents, and Using CLI + Gateway Together
Level: Intermediate
Estimated Time: ~75 minutes
Prerequisites: Hermes Agent v0.15.1, dashboard running, at least one gateway configured (Telegram or Discord from earlier labs), and 5+ completed sessions eligible for sharing.

### Lab Objectives

By the end of this lab you will be able to:

1. Export a session transcript to a shareable Markdown file using `/save` and manual export.
2. Identify which sessions qualify as "shared" for the **Shared Session** badge counter.
3. Spawn a multi-user `delegate_task` that routes to another Hermes profile or user.
4. Verify that a **Team Delegate** call increments the lifetime counter.
5. Use the CLI and a gateway (Telegram) in the same workflow to advance **Cross Platform**.
6. Understand the API endpoints for session export and recent-unlock notifications.
7. Generate a PNG share card (1200×630) for social media from an unlocked badge.

### Why This Lab Matters

Hermes is not a solo tool. The Social & Community badges measure how well you integrate the agent into collaborative workflows. **Shared Session** surfaces work to teammates. **Team Delegate** distributes load across agents. **Cross Platform** ensures you are not locked into a single interface. On a 2015 MacBook Pro with 16 GB RAM, memory pressure makes it hard to run multiple local models at once — delegating heavy tasks to a teammate's machine or a remote server via `delegate_task` is a practical necessity, not just a badge hunt.

### Step-by-Step Instructions

#### Step 1: Check Your Current Social Badge Progress (5 minutes)

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | select(.id | IN("shared_session","team_delegate","cross_platform")) | {id, tier, progress, thresholds}'
```

Thresholds:
- **Shared Session:** Copper 5, Silver 15, Gold 40, Diamond 100, Olympian 250 (`lifetime`)
- **Team Delegate:** Copper 10, Silver 30, Gold 80, Diamond 200, Olympian 500 (`lifetime`)
- **Cross Platform:** Copper 2, Silver 3, Gold 4, Diamond 5, Olympian 6 (`lifetime`)

Note the current tier. For most learners, Shared Session and Cross Platform advance naturally once you understand what counts.

#### Step 2: Share a Session to File (10 minutes)

Inside a Hermes TUI session:

```
/save
```

This writes the transcript to `~/.hermes/sessions/<uuid>.jsonl`. To turn it into a shareable artifact:

```bash
mkdir -p ~/shared-hermes-sessions
cp ~/.hermes/sessions/$(ls -t ~/.hermes/sessions/ | head -1) ~/shared-hermes-sessions/
```

Then generate a Markdown summary:

```
Read the most recent session file in ~/shared-hermes-sessions/ and convert it to a readable Markdown summary. Save it to ~/shared-hermes-sessions/latest-summary.md
```

Sharing methods that count:
- Exporting to PDF via `pandoc`.
- Copy-pasting the `/save` output into a GitHub gist or Slack.
- Using the Hermes dashboard "Export" button (which fires the share event).

#### Step 3: Share via Dashboard and Generate a PNG Card (10 minutes)

Open `hermes dashboard` → Achievements tab. Click any unlocked badge. If v0.4.0+ is installed, a "Generate Share Card" button appears. Click it. The server renders a 1200×630 PNG using the badge name, tier, and current progress. Save it to:

```
~/Desktop/hermes-badge-share.png
```

This counts as a `shared_session` event in some configurations. Verify by checking the API again after the action.

#### Step 4: Team Delegate — Spawn a Subagent for Another User (20 minutes)

In Hermes TUI, delegate a task with an explicit target user:

```
delegate_task to user "teammate-profile" with the following task:
"Analyze the CPU temperature logs in ~/macbook-logs/ and return a one-sentence summary."
```

The exact syntax varies by client, but the principle is the same: the `delegate_task` tool receives a `target_user` parameter. If the target user is different from the caller, the counter increments. Thresholds:
- **Team Delegate:** Copper 10, Silver 30, Gold 80, Diamond 200, Olympian 500 (`lifetime`).

If you do not have a teammate profile, simulate it:

```python
# test_delegate.py
import json, os

delegate_event = {
    "tool": "delegate_task",
    "args": {"task": "Summarize ~/notes.txt", "target_user": "demo-user"},
    "caller": "hermes-learn"
}

log_path = os.path.expanduser("~/.hermes/delegate-test.log")
with open(log_path, "a") as f:
    f.write(json.dumps(delegate_event) + "\n")
print("Simulated team delegate logged.")
```

Run it:

```bash
python3 ~/test_delegate.py
```

Then force a rescan:

```bash
curl -X POST http://127.0.0.1:9119/api/plugins/hermes-achievements/rescan
```

#### Step 5: Cross Platform — Use CLI and Telegram in One Session (20 minutes)

Prerequisite: Telegram gateway running (see Lab 6).

1. Start a CLI session:

```bash
hermes --tui
```

2. Inside the session, send a message to your Telegram bot:

```
Use the telegram gateway to send "Cross-platform test initiated from CLI" to my chat.
```

3. Receive a reply on Telegram. Reply from Telegram.

4. Back in the CLI session, check if the Telegram reply was picked up:

```
Did any gateway messages arrive while I was away?
```

Each distinct platform used within the tracked lifetime period counts toward Cross Platform. Thresholds:
- **Cross Platform:** Copper 2, Silver 3, Gold 4, Diamond 5, Olympian 6 (`lifetime`).

If Telegram is unavailable, substitute Discord or the web dashboard message interface.

#### Step 6: Monitor Recent Unlocks via API (10 minutes)

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/recent-unlocks \
  | jq '.[] | {name, tier, unlocked_at}'
```

This endpoint returns the last 10 unlocked badges with ISO-8601 timestamps. If a social badge unlocked during this lab, it will appear here.

### Troubleshooting

- **`shared_session` not incrementing:** The old `/save` command alone does not always trigger the share counter. Use the dashboard "Export" button or share via a gateway message for reliable counting.
- **Team Delegate requires distinct users:** Delegating to yourself or to an anonymous subagent does not increment the badge. Verify that `target_user` is present and different from the caller.
- **Cross Platform counts platforms, not sessions:** Using CLI five times and Telegram once counts as 2 platforms, not 6. You need 6 *distinct* platforms for Olympian.
- **PNG share cards not rendering:** Ensure Hermes is v0.4.0+. The card generator uses headless Chrome; if Chrome is missing on your MacBook, install it via MacPorts: `sudo port install chromium`.

### Expected Outcome

- Shared Session progress increments by at least +1.
- Team Delegate progress increments by at least +1 (or is simulated and rescanned).
- Cross Platform progress shows at least 2 platforms (CLI + one gateway).
- You understand that social badges reward *integration* into teams and workflows, not raw volume.

### Lab 8 Use Case Completed

You have shared a session artifact, simulated a team delegation, and bridged CLI and gateway usage. Your Hermes agent is no longer a local-only tool — it is a node in a collaborative network. Even on a 2015 MacBook, delegation lets you offload heavy work to remote agents.

### Training Idea / Self-Improvement Focus

Social badges are the most "invisible" category because they depend on external people and systems. Set a weekly reminder: share one Hermes session summary with a colleague. After 15 weeks, you hit Silver on Shared Session. After 250 shares, you hit Olympian — and you will have built a library of reusable session artifacts. The badge is a side effect of a healthy documentation habit.

### Challenge (Recommended)

1. Create a cron job that runs every Monday at 9 AM and automatically shares the previous week's session summary to a Telegram group.
2. The cron job should:
   - Find the 5 most recent sessions in `~/.hermes/sessions/`.
   - Summarize them with `write_file`.
   - Send the summary to Telegram.
   - Log the share event so the badge counter increments.
3. Test the cron job manually with `hermes cron run`.

### Emotional Reward

**You have made Hermes a team player. Delegation is not laziness — it is architecture. Well done!**

---

## Chapter 8: How Social Achievements Are Tracked Across Gateways and Delegates

**Top Ideal Study Objectives:**
- Trace the `share` event from dashboard click to API call to state.json update.
- Understand how `delegate_task` records distinct target users for Team Delegate.
- Identify the platform registry that maps gateway IDs to Cross Platform counters.
- Connect the PNG share card renderer to the social badge pipeline.

**Description:**
This chapter examines the backend mechanisms behind the three Social & Community badges. Unlike session-quality badges, which inspect timestamps, social badges inspect *metadata*: who the session was shared with, who the delegate target was, and which gateway IDs appeared in the user's lifetime history. On a 2015 MacBook Pro with limited uplink bandwidth, the PNG card renderer is a local headless-Chrome job — it does not upload to a cloud. Sharing is a local file operation that *logs* an event, which the scanner later counts.

**Actions List (Topics):**
1. Locate the share event logger in the dashboard frontend or plugin API.
2. Identify the `delegate_task` metadata parser that extracts `target_user`.
3. Trace the platform registry (CLI, Telegram, Discord, Web Dashboard, Email, SMS).
4. Observe how the PNG card generator consumes badge state and produces a 1200×630 image.

**Full Source Code Snippets with Line-by-Line Explanations:**

```python
# hermes-achievements plugin: social_tracker.py (conceptual reconstruction)

class SocialTracker:
    PLATFORMS = {"cli", "telegram", "discord", "web_dashboard", "email", "sms"}

    def __init__(self, user_state: dict):
        self.state = user_state

    def log_share(self, session_id: str, method: str):
        """
        Called by the dashboard "Export" button or `/share` command.
        method: "dashboard_export", "gateway_send", "gist_upload", "pdf_render"
        """
        event = {
            "session_id": session_id,
            "method": method,
            "shared_at": datetime.utcnow().isoformat() + "Z"
        }
        self.state.setdefault("shared_sessions", []).append(event)   # Line ~22
        self.state["shared_session_count"] = len(self.state["shared_sessions"]) # Line ~23
        print(f"[Social] Share logged. Total: {self.state['shared_session_count']}") # Line ~24

    def log_delegate(self, task_id: str, caller: str, target: str):
        """
        Called by the delegate_task tool wrapper.
        Only increments if caller != target.
        """
        if caller == target:                                        # Line ~31
            print("[Social] Self-delegate does not count for Team Delegate.") # Line ~32
            return                                                  # Line ~33

        event = {
            "task_id": task_id,
            "caller": caller,
            "target": target,
            "delegated_at": datetime.utcnow().isoformat() + "Z"
        }
        self.state.setdefault("delegates", []).append(event)        # Line ~41
        self.state["team_delegate_count"] = len(self.state["delegates"]) # Line ~42

    def log_platform_use(self, platform_id: str):
        """
        Called at session start. platform_id must be in PLATFORMS.
        """
        if platform_id not in self.PLATFORMS:                       # Line ~49
            print(f"[Social] Unknown platform: {platform_id}")      # Line ~50
            return                                                  # Line ~51

        used = self.state.setdefault("platforms_used", set())       # Line ~54
        used.add(platform_id)                                       # Line ~55
        self.state["platforms_used"] = used                         # Line ~56
        self.state["cross_platform_count"] = len(used)              # Line ~57

# Line-by-line:
# Line 22-24 : The share event is appended to a list and the counter is
#              recomputed from list length. This is slightly expensive for
#              Olympian (250 shares) but trivial on a 2015 MacBook.
#              The list preserves provenance; the counter is a convenience.
#
# Line 31-33 : Self-delegation guard. If you delegate to your own profile,
#              the tool executes but the social tracker skips the increment.
#              This prevents gaming by spawning fake subagents.
#
# Line 41-42 : Legitimate delegates are logged with caller and target.
#              The counter is len(delegates), not len(unique targets).
#              You can delegate to the same teammate 500 times and still
#              reach Olympian.
#
# Line 49-51 : Platform whitelist. Invalid platform IDs (e.g., a misspelled
#              "telegam") are silently ignored. This prevents pollution.
#
# Line 54-57 : A set deduplicates platforms. CLI + Telegram + Discord = 3.
#              Repeating Telegram does not increment. The set is serialized
#              to JSON list in state.json because JSON has no native set.
```

**Master Prompt for This Chapter:**

```
You are continuing my Hermes Agent deep-dive education from Chapter 8.
Explain the Social & Community tracking pipeline:
- When I click "Export" in the dashboard, which function is called (Line 22),
  and what data structure stores the share history?
- If I delegate a task to myself, does Team Delegate increment? Which line
  enforces this rule, and why is it necessary?
- Cross Platform uses a set (Line 54). If I first use CLI, then Telegram,
  then CLI again, what is the value of cross_platform_count after each step?
- The PNG share card renderer reads state.json. If I delete state.json and
  force a rescan, will the share card still show my badges? Why or why not?
- How many distinct platform IDs are defined in PLATFORMS, and which two are
  the easiest for a solo developer to unlock on a 2015 MacBook Pro?
Use a 2015 MacBook Pro as the hardware context.
Conclude with exactly 5 questions to test my understanding.
```

**Chapter Conclusion — What You Have Learned**

1. Shared Session tracks export events, not file saves. Using the dashboard "Export" button is the most reliable way to increment.
2. Team Delegate requires a distinct caller and target. Self-delegation is explicitly filtered out to prevent badge farming.
3. Cross Platform uses a set, not a counter. Repeated use of the same platform does not help; you must expand to new interfaces.
4. Social badges are metadata-driven. The scanner inspects session headers and tool wrappers, not message content.
5. PNG cards are local renders. They work offline, which is ideal for a 2015 MacBook that may not always have reliable Wi-Fi.

**5 Questions to Check Your Understanding:**

1. You run `hermes --tui` (CLI) and inside it delegate a task to yourself. Which social badge counters, if any, increment? Explain using Lines 31-33 and 54-57.
2. If the `shared_sessions` list contains 250 events but `shared_session_count` is 247, what is the most likely cause, and how would you fix it?
3. You have used CLI, Telegram, Discord, and Web Dashboard. What tier is Cross Platform, and how many more platforms do you need for Olympian?
4. The PNG share card generator fails with a "Chrome not found" error on your MacBook. What is the exact MacPorts command to fix it, and which version of Hermes introduced PNG cards?
5. A teammate delegates a task *to* you via `delegate_task`. Does this increment *your* Team Delegate counter, *theirs*, both, or neither? Explain the directionality of the event log.
