# LangGraph — Simple Chatbot

## Definition

**LangGraph** is a library (built on top of LangChain) for building stateful, multi-step LLM applications as a **graph** of nodes and edges, instead of a single linear chain. Each **node** is a Python function that does some work (e.g. call an LLM), and **edges** define how control flows from one node to another.

A **Simple Chatbot** in LangGraph is the most basic graph:
- One shared **State** (a dictionary-like object) that flows through the graph.
- One **node** that calls the LLM with the current messages.
- `START -> node -> END` edges.
- The graph is **compiled** into a runnable object.

### Key building blocks

| Concept | What it means |
|---|---|
| `StateGraph(State)` | Creates a graph whose data flows through a defined `State` schema |
| `State` (TypedDict) | Shared memory/schema for the graph — every node reads/writes to it |
| `Annotated[list, add_messages]` | Marks the `messages` field as a list that should be **appended to**, not overwritten |
| `add_messages` | A **reducer** function — decides *how* new node output is merged into existing state (here: append new messages instead of replacing) |
| Node | A plain function `(state) -> partial_state_update` |
| `add_node("name", fn)` | Registers a function as a node in the graph |
| `add_edge(START, "node")` | Defines control flow (which node runs after which) |
| `compile()` | Turns the graph definition into an executable graph object |
| `graph.invoke({...})` | Runs the graph once with an initial state |

### Why the reducer (`add_messages`) matters
Without a reducer, returning `{"messages": [new_msg]}` from a node would **overwrite** the whole `messages` list in state. `add_messages` tells LangGraph to **append** the new message(s) to the existing conversation history instead of replacing it — this is what gives the chatbot its running conversation.

---

## Code (minimal)

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model

# 1. Define shared state
class State(TypedDict):
    messages: Annotated[list, add_messages]   # reducer = append, not overwrite

# 2. LLM
llm = init_chat_model("groq:qwen/qwen3.8-27b")

# 3. Node function
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 4. Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 5. Compile
graph = graph_builder.compile()

# 6. Run
response = graph.invoke({"messages": ["Hi, my name is Vivek"]})
for m in response["messages"]:
    m.pretty_print()
```

---

## Likely interview questions
## LangChain vs LangGraph

 - **LangChain:** Helps build LLM applications using chains, tools, prompts, agents, etc.
- **LangGraph:** Helps build **stateful, multi-step workflows/agents** as graphs with nodes and edges.

 ## Why do we need a `State` schema?

 `State` defines the **data shared between nodes** in the graph.

 A **reducer** tells LangGraph **how to update a state field** when a node returns a new value.

 ## What if you don't use `add_messages`?

 Without `add_messages`, the `messages` field is usually **overwritten** instead of having new messages appended/merged correctly.

 `add_messages` handles adding and updating messages properly.

 ## What is a node?

 A **node** is a function that performs a task in the graph.

 It receives the current `State` and must **return a state update**, usually as a dictionary.

```
def my_node(state):
    return {"messages": ["Hello"]}
```

 ## `add_edge` vs Conditional Edges

 - **`add_edge`:** Always follows a fixed path from one node to another.
- **Conditional edge:** Chooses the next node **based on the current state or some condition**.

```
add_edge:
A → B

conditional:
A → B
  → C
```
