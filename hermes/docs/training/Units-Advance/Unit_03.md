# Unit 03 — Model Diversity
> **Scope:** Model & Provider Lore: multi-model sessions and provider exploration badges.
> **System:** Hermes Agent v0.15.1  
> **Hardware Context:** 2015 MacBook Pro, 16 GB RAM, macOS Ventura

---

## Lab (Operator-Focused / CLI Hands-On)

### 1. Prerequisites
- Hermes Agent v0.15.1 on a 2015 MacBook Pro (16 GB RAM, macOS Ventura).
- Active API keys for at least 3 providers (e.g., Anthropic, Ollama Cloud, OpenRouter).
- Local Ollama installed (Intel Mac build) OR a lightweight local model endpoint.
- Familiarity with `/model` or `hermes --model` to switch providers mid-session.
- Stable internet connection capable of handling concurrent API streams on older Wi-Fi hardware.

### 2. Objectives
By the end of this lab you will:
- Use 5+ models in a single session to trigger `five_model_flight`.
- Register 3 distinct providers toward `provider_polyglot` Copper.
- Run model-specific sessions for `claude_confidant`, `gemini_cartographer`, and `open_weights_pilgrim`.
- Verify progress via the Achievements Dashboard API.

### 3. Why It Matters
Model diversity is not vanity—it improves response quality by matching the right architecture to each task. On a 2015 MacBook Pro, local models (Ollama CPU inference) are slower but incur zero token cost and work offline. Remote providers fill capability gaps without loading heavy weights into 16 GB RAM.

### 4. Step-by-Step with EXACT Commands

**4.1 Badge Tier Reference Table**

| ID | Name | Kind | Metric | Copper | Silver | Gold | Diamond | Olympian |
|---|---|---|---|---|---|---|---|---|
| `five_model_flight` | Five-Model Flight | `best_session` | 5+ models used in one session | — | — | — | — | — |
| `provider_polyglot` | Provider Polyglot | `lifetime` | Distinct providers used | 3 | 5 | 8 | 12 | 18 |
| `claude_confidant` | Claude Confidant | `lifetime` | Claude-specific sessions | 50 | 150 | 400 | 1,000 | 3,000 |
| `gemini_cartographer` | Gemini Cartographer | `lifetime` | Gemini-specific sessions | 50 | 150 | 400 | 1,000 | 3,000 |
| `open_weights_pilgrim` | Open Weights Pilgrim | `lifetime` | Local/OSS model sessions | 50 | 150 | 400 | 1,000 | 3,000 |

**4.2 Enumerate available providers**
```bash
hermes providers list
```
On a 2015 MBP running Ventura, expect Ollama (local), Anthropic, and OpenRouter by default after API keys are exported:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENROUTER_API_KEY="sk-or-..."
```

**4.2 Start a Five-Model Flight session**
Inside Hermes `/model` interface, switch sequentially:
```
/model claude-sonnet-4-20250514
/model kimi-k2.6
/model glm-5.1
/model qwen3-235b-a22b
/model gemini-2.5-pro
```
After each switch, send at least one message (e.g., "Summarize the previous step in one sentence"). The `best_session` metric tracks distinct models used inside a single saved session. On a 2015 machine, wait for each model to finish before switching to avoid queuing too many concurrent streams.

**4.3 Provider Polyglot (lifetime distinct providers)**
Run one session with each provider:
```bash
# Session A — Anthropic
hermes --model claude-sonnet-4-20250514

# Session B — Ollama (local)
hermes --model ollama/llama3.1:8b

# Session C — OpenRouter / DeepSeek
hermes --model openrouter/deepseek-chat
```
Each distinct provider increments the lifetime counter. Copper requires only 3; Gold requires 8, which means exploring every provider Hermes supports.

**4.4 Claude Confidant**
Set Claude as the default model for a week:
```bash
hermes --model claude-sonnet-4-20250514
```
Each saved session counts. Copper is 50 sessions; on a daily driver workflow, that takes roughly two months. Speed-run by running short `read_file` or `terminal` micro-sessions and typing `/save`.

**4.5 Gemini Cartographer**
```bash
hermes --model gemini-2.5-pro
```
Same pattern as Claude Confidant. Google’s Gemini is especially useful for long-context tasks (up to 1M tokens), which complements the 2015 MBP’s limited RAM.

**4.6 Open Weights Pilgrim**
```bash
# Start local Ollama (CPU inference on 2015 dual-core i7)
ollama run llama3.1:8b

# Then open a Hermes session targeting local Ollama endpoint
hermes --model ollama/llama3.1:8b
```
each saved session with a local/OSS model increments the counter. Note: on a 2015 MBP, stick to 7B–8B parameter models. Running 70B via CPU would swap aggressively and overheat.

**4.7 Verify progress via API**
```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements \
  | jq '.achievements[] | select(.category == "Model & Provider Lore") | {id, tier, progress, thresholds}'
```

### 5. Troubleshooting
| Symptom | Fix |
|---------|-----|
| `/model` returns "provider not found" | Check API keys in environment and `~/.hermes/config.yaml`. |
| Local Ollama runs out of RAM | Use 7B or 8B models only; quit Safari tabs to free memory. |
| Five-Model Flight not triggering | Ensure all 5 switches occur inside the same saved session. |
| Long latency on 2015 Wi-Fi | Switch off Bluetooth or use Ethernet dongle to reduce interference. |
| Dashboard shows `null` tier | Wait for the next background scan after `/save`. |

### 6. Expected Outcome
You will see at least one model-specific badge at Copper tier and `provider_polyglot` at Copper (3 providers). Five-Model Flight will appear as Unlocked if the session included 5+ distinct models.

### 7. Use Case Completed
A researcher on a 2015 MBP uses Claude for analysis, Gemini for long-document summarization, and local Llama for offline brainstorming. Tracking Model Diversity badges gamifies responsible multi-model habits.

### 8. Training Idea
Create a weekly "Model Rotation Tuesday": alternate default models every Tuesday. This naturally pushes `claude_confidant`, `gemini_cartographer`, and `open_weights_pilgrim` forward in parallel.

### 9. Challenge
Reach **Gold** on `provider_polyglot` (8 providers) and **Copper** on all three model-specific badges within 60 days on a 2015 MacBook Pro with 16 GB RAM and no GPU.

### 10. Emotional Reward
The first time you switch from a cloud model to a local 8B model on a plane with no Wi-Fi—and it still answers beautifully—you understand why `open_weights_pilgrim` exists.

---

## Chapter (Architect-Focused / Code & Internals)

### 1. Top Objectives
- Map the Model & Provider Lore schema to provider IDs and model family strings.
- Build a local session logger that records which model handled each turn.
- Automate provider-switch prompts to guarantee Five-Model Flight in long sessions.

### 2. Description
Model & Provider Lore contains 5 achievements: one `best_session` (`five_model_flight`) and four `lifetime` counters (`provider_polyglot`, `claude_confidant`, `gemini_cartographer`, `open_weights_pilgrim`). The plugin parses `state.db` rows for `model_id` and `provider_id`. On Hermes v0.15.1, the evaluator normalizes model strings (e.g., `kimi-k2.6`, `glm-5.1`, `qwen3-235b-a22b`, `gemini-2.5-pro`) into a per-session set. If that set’s cardinality reaches 5, the badge fires. For lifetime counters, each session increments the tally for its active provider ID and, when applicable, the model-family bucket.

### 3. Actions List
1. Query `/achievements` and filter for Model & Provider Lore.
2. Read `~/.hermes/state.db` (SQLite) to inspect `model_id` and `provider_id` per message.
3. Build a CLI helper that prepends `/model <name>` to a batch of prompts.
4. Export a monthly chart of provider usage to guide cost optimization.
5. Write a cronjob that reminds you to switch models if 3 consecutive sessions used the same provider.

### 4. Full Source Code Snippet with Line-by-Line Explanations
```python
#!/usr/bin/env python3
# model_flight_helper.py — automate provider switching inside a Hermes session
import json, os

# Step 1: Define the 5-model roster optimized for a 2015 MBP
# (4 cloud models + 1 lightweight local model)
ROSTER = [
    "claude-sonnet-4-20250514",
    "kimi-k2.6",
    "gemini-2.5-pro",
    "openrouter/deepseek-chat",
    "ollama/llama3.1:8b"
]

# Step 2: Build a "prompt deck" — one message per model
workload = "Explain the concept of incremental scan caching in 2 sentences."
prompts = []
for idx, model in enumerate(ROSTER, start=1):
    # Each prompt prefixed with /model so Hermes switches providers
    prompts.append(f"/model {model}\n{workload} (turn {idx}/5)")

# Step 3: Write prompts to a batch file for copy-paste into Hermes TUI
batch_path = os.path.expanduser("~/hermes_five_model_batch.txt")
with open(batch_path, "w") as f:
    f.write("\n---\n".join(prompts))

print(f"Batch written to: {batch_path}")
print(f"Models in flight: {len(ROSTER)}")
print("Instructions: Paste each block (between --- delimiters) into Hermes.")
```
- **Step 1:** The roster blends remote APIs (fast, high capability) with one local model (offline, low RAM). On a 2015 MBP, the local model is intentionally 8B to avoid CPU thrashing.
- **Step 2:** Prefixing `/model <name>` forces Hermes to switch before processing the workload. Each switch counts toward the session’s distinct-model set.
- **Step 3:** Writing to a flat file lets the user paste sequentially without memorizing commands. The `---` delimiter makes chunking obvious in any TUI.

### 5. Master Prompt (Ready-to-Copy for Kimi-K2.6)
```
You are a Hermes Agent coach. The user is working on Unit 03: Model Diversity.
They run Hermes v0.15.1 on a 2015 MacBook Pro with 16 GB RAM.

Task:
1. List the 5 Model & Provider Lore badge IDs, their kinds, and their thresholds (all tiers).
2. Recommend a 5-model roster that works well on a 2015 MBP (intel CPU, 16 GB RAM, no GPU).
3. Provide a single-session transcript template that triggers Five-Model Flight without exceeding RAM.
4. Write a Python snippet that queries the API and prints the top under-leveled model-specific badge.
5. End with a one-line zsh alias to launch Hermes with the least-used provider today.
```

### 6. Conclusion
- `five_model_flight` rewards breadth in a single session; plan your roster ahead of time rather than improvising switches.
- `provider_polyglot` is lifetime-cumulative; every new provider you try permanently advances the counter.
- On a 2015 MBP, local models are viable but capped at ~8B parameters; use cloud models for heavy reasoning.
- `claude_confidant`, `gemini_cartographer`, and `open_weights_pilgrim` encourage loyalty to specific model families. Rotate weekly to avoid over-investing in one badge while neglecting others.
- The plugin’s model-family normalization means `gemini-2.5-pro` and future Gemini versions may count toward the same cartographer bucket—check release notes when new models ship.

### 7. Architecture Note
Provider metadata is stored in `state.db` as JSON columns on the `messages` table. The achievements plugin scans these rows incrementally and hashes `(session_id, provider_id, model_id)` tuples to avoid double-counting restarts or edits. Because disk I/O on a 2015 SATA SSD is modest, the plugin caps concurrent scans to one background thread.

### 8. Integration Checklist
- [ ] At least 3 distinct providers show `unlocked: true` in Dashboard API.
- [ ] One session contains messages from 5+ distinct models in `state.db`.
- [ ] `provider_polyglot` lifetime counter increments after trying a new provider.
- [ ] Local Ollama endpoint responds within 30 seconds on `ollama/llama3.1:8b`.
- [ ] API tier query returns non-null for all Model & Provider badges.

---

## Questions
1. What is the exact `kind` tracking type for `five_model_flight`, and what condition triggers it?
2. How many distinct providers are required to reach Diamond tier in `provider_polyglot`?
3. On a 2015 MacBook Pro with 16 GB RAM, why is the local model in the 5-model roster capped at 8B parameters?
4. Which three badges in this unit are family-specific (Claude, Gemini, Open Weights)?
5. What JSON column in `state.db` stores the model and provider metadata scanned by the plugin?
