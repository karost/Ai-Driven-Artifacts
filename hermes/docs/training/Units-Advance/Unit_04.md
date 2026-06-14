# Unit 4: Memory & Research — Web Search, Docs Archaeology, and Persistent Memory

> **Badges covered:** `rabbit_hole_certified`, `citation_goblin`, `docs_archaeologist`, `search_orchestrator`, `memory_keeper`, `memory_palace`, `context_dragon`

## Lab 4: Research Deep-Dive + Memory Persistence Marathon

Level: Advanced  
Estimated Time: ~90 minutes  
Prerequisites: Units 1–3 complete (CLI/TUI, model switching, basic memory).

### Lab Objectives

By the end of this lab you will be able to:

- Perform 20+ sequential `web_search` calls and 10+ `web_extract` calls to unlock `rabbit_hole_certified` and `citation_goblin`.
- Navigate documentation with `browser_navigate` and `read_file` to score `docs_archaeologist`.
- Trigger 50+ web calls in a single session for `search_orchestrator`.
- Write structured memories with the `memory` tool to progress `memory_keeper` and `memory_palace`.
- Trigger context-compression and memory consolidation cycles for `context_dragon`.
- Inspect your `~/.hermes/state.db` and achievement progress via the dashboard API.

### Why This Lab Matters

On a 2015 MacBook Pro with 16 GB RAM, every web lookup is orchestrated in the cloud — your machine is the conductor, not the orchestra. This lab teaches you how to turn Hermes into a research machine that remembers everything it learns. The badges here represent the core competency of any autonomous agent: information retrieval + persistent recall. Without research skills, the agent is blind. Without memory, it is amnesiac.

### Step-by-Step Instructions

#### Step 1: Open a Fresh Session and Set a Research Goal (5 minutes)

```bash
hermes --new
```

Type:
```
We are doing an advanced research marathon. Our topic: "Vector database comparison in 2026 — Qdrant vs Milvus vs Weaviate vs pgvector." Stay in this topic. I will approve every web call.
```

#### Step 2: Execute 20 Web Searches (25 minutes)

Run these exact commands inside the chat, one by one:

```
web_search: "Qdrant vector database 2026 benchmarks"
```
```
web_search: "Milvus 2026 performance comparison"
```
```
web_search: "Weaviate vs Qdrant latency benchmark"
```
```
web_search: "pgvector PostgreSQL vector extension limitations 2026"
```
```
web_search: "ANN algorithm HNSW vs IVF 2026"
```

Continue until you hit at least 20 distinct `web_search` calls. Vary queries by adding "architecture", "pricing", "scalability", "on-premise", "managed cloud", and "RAM usage".

**Troubleshooting:** If a search returns no results, rephrase keywords. If your Ollama Cloud rate limit triggers, pause 5 minutes and send a non-web message.

#### Step 3: Extract 10 Sources with web_extract (20 minutes)

For the top 10 URLs returned in Step 2, run:

```
web_extract: "https://qdrant.tech/documentation/..."
```

Type the exact URL. Repeat 10 times. Aim for doc pages, blog posts, and GitHub READMEs.

#### Step 4: Read Local Documentation Files (10 minutes)

From Terminal (outside chat), find any docs already on disk:

```bash
find ~ -type f -name "*.md" | head -30
```

Back in chat, run `read_file` on 5+ long Markdown files:

```
read_file: "/Users/thanit/work/hermes-dev/hermes-learn/docs/hermes-achievements-training.md"
```

Each `read_file` counts toward `docs_archaeologist`. On a 2015 MacBook, read local files first — they are instant and do not consume cloud quota.

#### Step 5: Write Memory Entries After Each Insight (10 minutes)

After every 3-4 searches, type:

```
memory: {"action": "save", "category": "research", "content": "Qdrant uses HNSW by default with configurable m and ef parameters. Best for <1M vectors on 16GB RAM."}
```

Vary categories: `research`, `hardware`, `vector_db`, `pricing`. Write at least 8 memory entries.

#### Step 6: Compress Context and Verify Dashboard (10 minutes)

Trigger context compression manually:

```
Compress my session context now.
```

Exit the chat (`/quit`) and check progress:

```bash
curl -s http://127.0.0.1:9119/api/plugins/hermes-achievements/achievements | jq '.achievements[] | select(.name=="Rabbit Hole Certified" or .name=="Citation Goblin" or .name=="Docs Archaeologist") | {name, progress, unlocked}'
```

#### Step 7: Resume and Test Recall (5 minutes)

```bash
hermes --continue
```

Ask: `What vector databases did we research and what did we conclude about Qdrant on 16GB RAM?`

If memory works, Hermes will parrot back stored entries.

### Expected Outcome

- 20+ web calls completed (progress toward Rabbit Hole Certified — Copper is 400 lifetime, but 20 is a strong start).
- 10+ `web_extract` calls completed.
- 5+ documentation files read.
- 8+ memory entries saved.
- Dashboard shows upward progress on at least 5 badges.
- Agent correctly recalls research conclusions after resuming.

### Lab 4 Use Case Completed

You treated Hermes as a dedicated research analyst. It searched, extracted, read docs, and wrote memories — all while you monitored progress on a real badge board. Your 2015 MacBook Pro handled the orchestration load without breaking a sweat.

### Training Idea / Self-Improvement Focus

- The Curator will scan this session in 7 days. If the memory entries are structured (category + timestamp + content), it may extract a reusable `vector_db_research` skill.
- `context_dragon` unlocks with 5,000 lifetime context events. Frequent compression and long sessions accelerate this.
- Consider using `delegate_task` for parallel research threads in Unit 5.

### Challenge (Recommended)

1. In one session, hit 50 web calls for `search_orchestrator` Copper (50 max in one session).
2. Create a memory entry after EVERY single web call.
3. Export your memory store:
   ```bash
   sqlite3 ~/.hermes/memory_store.db ".dump" > ~/research_memory_dump.sql
   ```
4. Import it into a spreadsheet and count how many categories you used.

### Emotional Reward

🏆 You just turned a 2015 MacBook into a research engine with a photographic memory. Every search, every extract, every doc read is now a badge on your wall.

---

## Chapter 4: The Research & Memory Stack — How Hermes Never Forgets

**Top Ideal Study Objectives:**
- Trace a web call from the CLI through the search module to the model response.
- Understand how `memory` tool writes to both SQLite and HRR vectors.
- See why local docs (read_file) and remote docs (browser_navigate) share the same pipeline.
- Connect context compression to `context_dragon` progress.

**Description:**
This chapter is the architect-level view of the research and memory subsystems. Lab 4 was operator-focused: you ran the tools. This chapter explains the wiring: how `web_search` resolves to a provider, how `memory` persists, and why your old MacBook can offload network I/O without blocking the event loop.

**Actions List (Topics):**
1. Locate the web search adapter in the source tree.
2. Trace a `memory` save from CLI to SQLite + HRR storage.
3. Read the context compression pseudocode.
4. Map each badge metric to the exact function that increments it.

**Full Source Code Snippets with Line-by-Line Explanations:**

```python
# research_memory.py  --  Educational pseudocode for the web + memory pipeline
# Version: v0.15.1+

"""
Research & Memory orchestrator.

This module handles:
  - web_search, web_extract, browser_navigate
  - memory save / recall / list
  - docs_archaeologist counting (local doc reads)
  - context compression triggering

It is fully async so a 2015 MacBook Pro does not block Terminal
while waiting for Ollama Cloud model responses or HTTP downloads.
"""

import asyncio           # Line ~10  --  non-blocking I/O for all web calls
import sqlite3           # Line ~11  --  local state persistence
import json              # Line ~12  --  memory payload serialization
from typing import Dict  # Line ~13  --  type safety for memory records

# Line-by-line:
# asyncio   : Every web_search is wrapped in an asyncio Task. This means
#             you can fire 10 searches and they multiplex over a single
#             event loop — critical on dual-core 2015 CPUs.
# sqlite3   : Memory and achievements are stored locally. No cloud DB
#             required. Your data stays on your SSD.
# json      : Memory entries are JSON blobs with schema:
#             {category, content, created_at, source_session_id}
# typing    : Enforces contract between tools and storage layers.

# ---- Memory save implementation ----
# Called by the memory tool after every approved save.

async def save_memory(payload: Dict[str, str]) -> str:
    conn = sqlite3.connect("~/.hermes/memory_store.db")   # Line ~25
    cursor = conn.cursor()                                 # Line ~26
    cursor.execute("""
        INSERT INTO memories (category, content, created_at)
        VALUES (?, ?, datetime('now'))
    """, (payload["category"], payload["content"]))       # Line ~30
    conn.commit()                                          # Line ~31
    conn.close()                                           # Line ~32
    return f"Memory saved: {payload['category']}"          # Line ~33

# Line ~25 : Opens the SQLite DB. On first run it auto-creates tables.
# Line ~30 : Parameterized query prevents SQL injection from any model
#            output that might attempt prompt-injection.
# Line ~31 : commit() is synchronous but the connection is local SSD.
#            On a 2015 MacBook Pro SSD, this is <1ms.
# Line ~33 : Returns confirmation to the model so it knows the save
#            succeeded and can decide to reference it later.

# ---- Context compression trigger ----
# Called when session message count exceeds threshold (default ~120).

async def maybe_compress(session_messages: list) -> list:
    if len(session_messages) > COMPRESS_THRESHOLD:        # Line ~40
        summary = await model.summarize(session_messages)   # Line ~41
        return [{"role": "system", "content": summary}]     # Line ~42
    return session_messages                                # Line ~43

# Line ~40 : Threshold is tunable in config.yaml under
#            memory.compression_threshold.
# Line ~41 : Offloads summarization to Ollama Cloud so the local CPU
#            is not burdened with long-context inference.
# Line ~42 : Replaces the long message list with a single summary.
#            This is what unlocks context_dragon progress.
```

**Master Prompt for This Chapter:**

Copy and paste into Kimi-K2.6 / Claude / GPT:

```
You are continuing my Hermes Agent deep-dive education from Chapter 4.
Explain the research and memory architecture:
1. Why is asyncio crucial for web_search on a 2015 MacBook Pro?
2. How does save_memory prevent SQL injection from model outputs?
3. What is the exact JSON schema of a memory payload?
4. When does maybe_compress trigger, and how does it relate to
debugging large sessions on old hardware?
5. Which badge metrics are incremented after web_search vs read_file?
Conclude with exactly 5 questions to test my understanding.
```

**Chapter Conclusion — What You Have Learned**

1. `web_search` and `memory` share the same async event loop, which is why your Terminal stays responsive on a 2015 MacBook.
2. SQLite is the ground truth for memory, but future retrieval uses HRR (Holographic Reduced Representation) vectors for semantic similarity.
3. Context compression is not just a memory optimization — it is a tracked metric (`context_dragon`) that gamifies good session hygiene.
4. Local file reads (`read_file`) and browser navigation (`browser_navigate`) both count toward documentation badges because they represent "information foraging" behavior.
5. The achievement scanner reads `~/.hermes/state.db` incrementally, so every badge you earn updates sub-second.

**5 Questions to Check Your Understanding:**

1. If you ran 10 `web_search` calls synchronously on a 2015 dual-core MacBook, what would happen to Terminal responsiveness? How does asyncio solve this?
2. Why does `save_memory` use parameterized SQL `(?, ?, ?)` instead of Python f-strings? What threat model does this mitigate?
3. `docs_archaeologist` tracks documentation reads. Does `read_file` on a local README count the same as `browser_navigate` to a remote docs page? Explain the scanner logic.
4. Your session hit 130 messages and `maybe_compress` triggered. What is the output of the function and how does it affect the achievement scanner's view of `context_dragon`?
5. You want to export all memories in category "research" to a JSON file. Write the exact sqlite3 command a 2015 MacBook user would run in Terminal.
