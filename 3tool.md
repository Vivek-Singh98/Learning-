````
# LangChain Tools — Interview Notes

## 1. What is a Tool?

A **Tool** is a Python function that an LLM can call to perform a specific task.

Examples:
- Get weather
- Search a database
- Call an API
- Perform calculations

---

## 2. Creating a Tool with `@tool`

```python
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city} is sunny."
````

 ### Important

 - `@tool` converts a Python function into a LangChain Tool.
- The **docstring** tells the LLM what the tool does.
- Type hints define the input type.

---

 ## 3\. Using `bind_tools()`

```
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini"
)

model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke(
    "What is the weather in Delhi?"
)

print(response.tool_calls)
```

 ### What does `bind_tools()` do?

 `bind_tools()` makes the tool available to the LLM.

 The LLM can decide:

```
User Question
      ↓
     LLM
      ↓
Tool needed?
      ↓
  Tool Call
```

 Example tool call:

```
Tool: get_weather
Arguments: {"city": "Delhi"}
```

 > `bind_tools()` mainly allows the LLM to generate a tool call.\
>  It does not automatically manage the complete tool-calling loop.

---

 ## 4\. Using `create_agent()`

```
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"The weather in {city} is sunny."

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the weather in Dehradun?"
        }
    ]
})

print(response["messages"][-1].content)
```

 ### Agent Flow

```
User
  ↓
LLM
  ↓
Decides to call Tool
  ↓
Tool
  ↓
Tool Result
  ↓
LLM
  ↓
Final Answer
```

---

 ## 5\. `bind_tools()` vs `create_agent()`

 | `bind_tools()` | `create_agent()` |
| --- | --- |
| Gives tools to the LLM | Creates an agent with tools |
| LLM can generate tool calls | Agent manages tool-calling workflow |
| More manual control | More automatic |
| Useful for learning tool calls | Useful for tool-based applications |

---

 ## 6\. Normal LLM vs Tool vs Agent

 ### Normal LLM

```
response = model.invoke("Hello")
```

 Only the LLM generates the response.

---

 ### LLM + Tool

```
model_with_tools = model.bind_tools([get_weather])
```

 LLM can decide to call a tool.

---

 ### Agent + Tool

```
agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather]
)
```

 Agent manages:

```
LLM → Tool → Tool Result → LLM → Final Answer
```

---

 ## 7\. Important Syntax

 ### Correct

```
load_dotenv()
```

 ### Wrong

```
load_dotenv
```

---

 ### Correct

```
system_prompt="You are a helpful assistant."
```

 ### Wrong

```
system_prompts="You are a helpful assistant."
```

---

 ### Correct

```
agent.invoke(...)
```

 ### Wrong

```
agent,invoke(...)
```

---

 ## 8\. Interview Questions

 ### Q1. What is a Tool?

 **Answer:**

 A Tool is a Python function that an LLM can call to perform a specific task, such as getting weather, calling an API, searching a database, etc.

---

 ### Q2. What does `@tool` do?

 **Answer:**

 `@tool` converts a normal Python function into a LangChain Tool that can be used by an LLM or Agent.

---

 ### Q3. What is `bind_tools()`?

 **Answer:**

 `bind_tools()` connects one or more tools with an LLM and allows the LLM to generate tool calls when needed.

---

 ### Q4. What is `create_agent()`?

 **Answer:**

 `create_agent()` creates an agent that can use tools and manage the tool-calling workflow to produce a final answer.

---

 ### Q5. Difference between `bind_tools()` and `create_agent()`?

 **Answer:**

 `bind_tools()` makes tools available to the LLM, while `create_agent()` manages the complete interaction between the LLM and tools.

---

 ## 9\. Easy Way to Remember

```
@tool
  ↓
Create a Tool

bind_tools()
  ↓
Give Tool to LLM

create_agent()
  ↓
LLM + Tools + Tool-calling Loop
```

---

 ## 10\. One-Line Interview Answer

 > A Tool is a function that an LLM can call to perform an external task. `bind_tools()` makes tools available to the LLM, while an Agent manages the tool-calling workflow.

```

```
