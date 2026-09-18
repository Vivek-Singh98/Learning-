# LangGraph — Human in the Loop (HITL)

## Definition

**Human-in-the-loop** means **pausing** the graph's execution at a specific node so a human can review, approve, edit, or provide input — then **resuming** the graph from exactly where it paused.

This is used for things like: approving a tool call before it runs (e.g. "send this email?"), letting a human correct/edit an LLM's draft, or asking the user a clarifying question mid-workflow.

It **requires a checkpointer** (memory) — because pausing and resuming later means the graph's state must be saved somewhere while waiting for the human.

### Key building blocks

| Concept | What it means |
|---|---|
| `interrupt(value)` | Called *inside* a node — pauses graph execution there and surfaces `value` to the caller/UI |
| `Command(resume=...)` | Used to **resume** a paused graph, injecting the human's response back into the interrupted node |
| Checkpointer (e.g. `MemorySaver`) | Required — stores the paused state so the graph can resume later, possibly after a long delay |
| `thread_id` | Identifies *which* paused conversation/run you are resuming |

### How the flow works
1. Graph runs normally until a node calls `interrupt("Please approve this action")`.
2. Execution **stops** there; the interrupt value is returned to the caller (e.g. shown in a UI).
3. The human reviews and responds.
4. You call `graph.invoke(Command(resume=human_response), config=config)` with the **same `thread_id`**.
5. The graph resumes inside that same node with the human's response, and continues to `END`.

---

## Code (minimal)

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

def human_approval_node(state: State):
    # Pause here and ask a human to approve
    decision = interrupt("Do you approve this action? (yes/no)")
    return {"messages": [f"Human said: {decision}"]}

graph_builder = StateGraph(State)
graph_builder.add_node("approval", human_approval_node)
graph_builder.add_edge(START, "approval")
graph_builder.add_edge("approval", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

# 1. Start the graph -> it will pause at interrupt()
result = graph.invoke({"messages": ["start task"]}, config=config)
print(result)   # contains the interrupt payload

# 2. Human reviews, then resume with their answer
final_result = graph.invoke(Command(resume="yes"), config=config)
print(final_result)
```

---

## Likely interview questions
## Why does Human-in-the-Loop require a checkpointer?

 A checkpointer **saves the graph state when it pauses**.\
 Without it, the graph cannot reliably **resume from where it stopped**.

 ## What does `interrupt()` do?

 `interrupt()` **pauses the graph and waits for human input**.

 You call it **inside a node**, at the point where human approval/input is needed.

```
from langgraph.types import interrupt

def approval_node(state):
    answer = interrupt("Approve this action?")
    return {"approved": answer}
```

 ## How do you resume a paused graph?

 Use `Command(resume=...)` with the **same `thread_id`**.

```
from langgraph.types import Command

graph.invoke(
    Command(resume="yes"),
    config={"configurable": {"thread_id": "123"}}
)
```

 The graph continues from the `interrupt()` point.

 ## Real HITL use case

 An agent wants to **send an email or make a payment**.

```
Agent → Prepare API call → Human approval → Execute API call
                              ↑
                          interrupt()
```

 The human can approve, reject, or modify the action before it happens.

 ## Before-node interrupt vs `interrupt()` inside a node

 - **Before-node interrupt:** Pauses **before the entire node runs**. Useful when you want approval before allowing a node to execute.
- **`interrupt()` inside a node:** The node **starts running and pauses at the exact point** where `interrupt()` is called.

 **Simple rule:**\
 `interrupt_before` = _“Should this node run?”_\
 `interrupt()` = _“I need human input at this point in the node.”_
