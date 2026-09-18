# MCP (Model Context Protocol) — Architecture & Transport

## Definition

**MCP (Model Context Protocol)** is a standard protocol that lets an LLM application connect to external **tools, data, and prompts** in a consistent way — instead of writing custom integration code for every tool.

### Core pieces

| Concept | What it means |
|---|---|
| **MCP Server** | Exposes **content, tools, and prompts** (e.g. `add`, `multiply`, a weather API) that an LLM app can call |
| **MCP Client** | Lives *inside* the host app; maintains a **1:1 connection** with one MCP server |
| **Host App** | The application the user interacts with (e.g. Claude Desktop, a custom chatbot). It can contain multiple MCP clients — one per server it talks to |
| **Tool** | A single function exposed by a server (decorated with `@mcp.tool()`), described with a name + docstring so the LLM knows what it does and when to call it |
| **Transport** | The communication channel between client and server — `stdio` or `streamable-http` |

### Overall flow
```
User input -> Host App (LLM) -> LLM decides: does it need a tool?
      -> if yes: MCP Client sends tool-call request to MCP Server (add/multiply/weather)
      -> MCP Server executes the tool, returns result
      -> Result goes back to the LLM -> LLM produces final answer -> shown to user
```

This is the same "ReAct" style loop LangGraph's `create_react_agent` implements: LLM reasons → decides to call a tool → tool runs → result fed back → LLM continues.

---

## Transport: `stdio` vs `streamable-http`

Transport = **how** the client and server actually exchange messages.

### `stdio` (Standard Input/Output)
- The **host app launches the server itself** as a local subprocess (e.g. runs `python mathserver.py`).
- Communication happens over that process's **stdin/stdout** streams — same idea as piping data between two command-line programs.
- No network involved — everything is on the same machine.
- Best for: local tools/scripts (math tool, local file tool) that only this one app needs.

### `streamable-http`
- The server is **already running independently** somewhere (a URL, e.g. `http://localhost:8000/mcp`, or deployed in the cloud).
- The client connects to it over **HTTP** and receives the response as a **stream of chunks** (similar to Server-Sent Events), rather than the server being spawned by the client.
- Multiple different clients/apps can connect to the same running server at once.
- Best for: remote tools/APIs (weather service, a shared internal tool server) that live outside the host app and may be reused by many clients.

| | `stdio` | `streamable-http` |
|---|---|---|
| Server lifecycle | Spawned/owned by the client | Runs independently, client just connects |
| Channel | Process stdin/stdout | HTTP request + streamed response |
| Network needed? | No (local only) | Yes |
| Typical use | Local tool/script | Remote/shared tool or API |

---

## Code (corrected & simplified)

**Packages:** `langchain-groq`, `langchain-mcp-adapters`, `mcp`

### `mathserver.py` (an MCP server, using `stdio`)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")   # server waits/responds via stdin-stdout
```

### `client.py` (host app: MCP client + LangGraph agent)
```python
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    tools = await client.get_tools()
    llm = ChatGroq(model="qwen/qwen3.8-27b")
    agent = create_react_agent(llm, tools)

    response = await agent.ainvoke({"messages": "what is 5 plus 10, then multiply by 20?"})
    for m in response["messages"]:
        m.pretty_print()

if __name__ == "__main__":
    asyncio.run(main())
```

> Fixes vs your draft: `MultiServerMCPClient` (not `MultiserverClient`), matching closing quotes/brackets on `args`, `def multiply(...)-> int:` (not `-->`), transport value is `"streamable_http"` (underscore, not `streamable_https`), and the weather `url` should be `http://` unless you've actually got TLS configured on `localhost`.

---

## Interview Questions & Answers

**Q1. What problem does MCP solve?**
A: Without MCP, every LLM app has to write custom glue code for every tool/API it wants to use. MCP standardizes this — any MCP-compatible client can talk to any MCP-compatible server the same way, so tools become plug-and-play.

**Q2. What is the difference between an MCP host, client, and server?**
A: The **host** is the user-facing app (e.g. Claude Desktop). The **client** lives inside the host and maintains a 1:1 connection to one server. The **server** exposes tools/content/prompts that the client can call. One host can run multiple clients — one per server.

**Q3. Why is the connection between client and server 1:1?**
A: Each client instance is dedicated to managing the session/state with exactly one server, keeping tool discovery and calls scoped and predictable; the host coordinates multiple such 1:1 client-server pairs (e.g. one for "math", one for "weather").

**Q4. What is the difference between `stdio` and `streamable-http` transport?**
A: `stdio` is used when the host spawns the server itself as a local subprocess and talks to it via standard input/output — no network. `streamable-http` is used when the server already runs independently (locally or remote) and the client connects to it over HTTP, receiving a streamed response — this allows multiple clients and remote/cloud servers.

**Q5. When would you choose `stdio` over `streamable-http`?**
A: Choose `stdio` for simple, local-only tools you fully control and only one app needs (fast, no network overhead). Choose `streamable-http` when the tool/service needs to be shared across multiple clients, deployed remotely, or scaled independently of the host app.

**Q6. In the flow "user input → LLM → tool call → LLM → output", who decides whether a tool is called?**
A: The **LLM** decides — based on the user's message and the tool descriptions (docstrings) it was given via `bind_tools`/`create_react_agent`, it chooses to emit a tool call instead of (or before) a final answer. The MCP client is just the mechanism that executes that call against the right server.

**Q7. What does the docstring on `@mcp.tool()` functions actually do?**
A: It's not just documentation — the LLM reads the function name, arguments, and docstring to understand **what the tool does and when to use it**. A vague/missing docstring makes the LLM less reliable at choosing the right tool.

**Q8. What is `MultiServerMCPClient` used for?**
A: It lets one host app manage connections to **multiple MCP servers at once** (e.g. "math" over stdio, "weather" over streamable-http), fetch all their tools with `get_tools()`, and hand them all to a single LangGraph agent.
