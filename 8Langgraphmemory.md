# LangGraph — Memory (Checkpointer)

## Definition

By default, a compiled LangGraph graph is **stateless between calls** — each `graph.invoke()` starts fresh, it doesn't remember earlier turns.

**Memory** in LangGraph is added using a **Checkpointer**. A checkpointer saves the graph's `State` after every step (a "checkpoint"), keyed by a **thread_id**. When you call the graph again with the same `thread_id`, LangGraph loads the last saved state and continues from there — giving the chatbot short-term / conversational memory.

### Key building blocks

| Concept | What it means |
|---|---|
| `MemorySaver` | The simplest built-in checkpointer — stores state **in-memory** (RAM), lost on restart |
| Checkpointer | Pluggable storage for graph state (in-memory, SQLite, Postgres, Redis, etc.) |
| `graph_builder.compile(checkpointer=memory)` | Wires the checkpointer into the compiled graph |
| `thread_id` | A unique ID representing one conversation/session — state is saved & loaded per thread |
| `config = {"configurable": {"thread_id": "1"}}` | Passed to `invoke`/`stream` so LangGraph knows *which* conversation's state to load/save |

### Why it matters
Without a checkpointer, every `invoke()` call is independent — the LLM has no idea what was said before. With a checkpointer + `thread_id`, calling the graph multiple times with the same `thread_id` continues the same conversation (LLM sees full message history), while a different `thread_id` starts a brand-new conversation.

This is also the foundation for **Human-in-the-loop** (you need saved state to pause and resume a graph).

---

## Code (minimal)

```python
from langgraph.checkpoint.memory import MemorySaver

# 1. Create a checkpointer
memory = MemorySaver()

# 2. Compile the graph WITH the checkpointer
graph = graph_builder.compile(checkpointer=memory)

# 3. Unique thread id = one conversation session
config = {"configurable": {"thread_id": "1"}}

# 4. First message
graph.invoke({"messages": ["Hi, my name is Vivek"]}, config=config)

# 5. Second call, SAME thread_id -> remembers earlier message
graph.invoke({"messages": ["What's my name?"]}, config=config)
```

> Note: the key is `thread_id`, not `thred` — a common typo to watch for.

---

## Likely interview questions
## Why is a LangGraph graph stateless by default?

 A graph does **not automatically remember previous runs**. Each run starts with a fresh state unless you configure a checkpointer.

 ## What is a checkpointer?

 A **checkpointer** saves the graph's state so it can be restored later.

 Common types:

 - `MemorySaver` → stores state in memory
- **SQLite** → persists state in a local database
- **Postgres** → persists state in a PostgreSQL database

 ## What is `thread_id` used for?

 `thread_id` identifies a **conversation/workflow thread** so LangGraph knows which saved state belongs to which user/session.

 It lives in the **checkpoint configuration**, for example:

```
config = {"configurable": {"thread_id": "user-123"}}
```

 ## How do you persist memory across app restarts?

 Use a **persistent checkpointer** such as **SQLite or Postgres** instead of `MemorySaver`.

 `MemorySaver` → lost when the application restarts.\
 SQLite/Postgres → state can survive restarts.

 ## How is memory related to human-in-the-loop?

 Memory allows the graph to **pause and resume with its previous state**.

 This is useful for human-in-the-loop workflows because a human can review/approve something, and the graph can later **continue from the saved state**.
