## LangChain

 **Definition:**\
 LangChain is a framework for building applications powered by **LLMs (Large Language Models)**. It provides tools and components to connect LLMs with **prompts, tools, APIs, databases, memory, and other services**.

 **Simple way to remember:**

 > **LangChain = Framework for building LLM-powered applications.**

---

 ## LangGraph

 **Definition:**\
 LangGraph is a framework for building **stateful, multi-step, and agent-based AI applications**. It represents an application as a **graph of nodes and edges**, where each node performs a task and the state can be maintained between steps.

 **Simple way to remember:**

 > **LangGraph = Framework for building complex, stateful AI workflows and agents.**

 ### Quick Difference

```
LangChain
   ↓
Build LLM applications
   ↓
Models + Prompts + Tools + RAG + Agents

LangGraph
   ↓
Build complex AI workflows
   ↓
Nodes + Edges + State + Agents
```

 **One-line interview answer:**

 > **LangChain helps you build applications around LLMs, while LangGraph helps you build complex, stateful, and multi-step agent workflows.**
>
> LangChain: Agents & Model Integration
1. Load API Keys

Use .env to store API keys safely.

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


Note: Make sure the variable name is OPENAI_API_KEY, not OPEN_API_KEY.

2. Create an Agent

An agent allows an LLM to use tools when necessary.

from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get the weather for this city."""
    return f"The weather of {city} is sunny"

agent = create_agent(
    model="gpt-5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)


Invoke the agent:

response = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is the weather in Dehradun?"}
    ]
})

print(response["messages"][-1].content)

Remember

Agent = LLM + Tools + Instructions

3. Using Different Models

LangChain provides init_chat_model() to initialize different chat models.

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1")

response = model.invoke("Hello, how are you?")
print(response.content)

4. OpenAI

Using init_chat_model():

model = init_chat_model("gpt-4.1")


Or directly:

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1")

5. Google Gemini

Using init_chat_model():

model = init_chat_model(
    "google_genai:gemini-2.5-flash-lite"
)


Or directly:

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)

6. Groq
from langchain_groq import ChatGroq

model = ChatGroq(
    model="qwen/qwen3-32b"
)

response = model.invoke("Hello, how are you?")
print(response.content)

Quick Revision
.env
 ↓
API Keys
 ↓
LangChain Model
 ↓
invoke()
 ↓
Response

Main concepts

OpenAI → ChatOpenAI

Google Gemini → ChatGoogleGenerativeAI

Groq → ChatGroq

Generic model initialization → init_chat_model()

Agent → Model + Tools + System instructions

invoke() → Send input and get complete response
