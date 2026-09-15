# LangChain: Agents & Model Integration

## 1. Load API Keys

Use `.env` to store API keys safely.

```python
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
````

 > **Note:** Make sure the variable name is `OPENAI_API_KEY`, not `OPEN_API_KEY`.

---

 ## 2\. Create an Agent

 An **Agent** allows an LLM to use tools when necessary.

```
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get the weather for this city."""
    return f"The weather of {city} is sunny"

agent = create_agent(
    model="gpt-5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)
```

 ### Invoke the Agent

```
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

 ### Remember

 > **Agent = LLM + Tools + Instructions**

---

 ## 3\. Using Different Models

 LangChain provides `init_chat_model()` to initialize different chat models.

```
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1")

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 ## 4\. OpenAI

 ### Using `init_chat_model()`

```
model = init_chat_model("gpt-4.1")
```

 ### Using `ChatOpenAI`

```
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1")

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 ## 5\. Google Gemini

 ### Using `init_chat_model()`

```
model = init_chat_model(
    "google_genai:gemini-2.5-flash-lite"
)
```

 ### Using `ChatGoogleGenerativeAI`

```
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 ## 6\. Groq

```
from langchain_groq import ChatGroq

model = ChatGroq(
    model="qwen/qwen3-32b"
)

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 # Quick Revision

```
.env
  ↓
API Keys
  ↓
LangChain Model
  ↓
invoke()
  ↓
Response
```

 ## Main Concepts

 - **OpenAI** → `ChatOpenAI`
- **Google Gemini** → `ChatGoogleGenerativeAI`
- **Groq** → `ChatGroq`
- **Generic model initialization** → `init_chat_model()`
- **Agent** → Model + Tools + System Instructions
- **invoke()** → Send input and get a complete response

 ## Easy Memory Trick

```
invoke()  → One input → Complete response

stream()  → One input → Chunks of response

batch()   → Multiple inputs → Multiple responses

Agent     → Model + Tools + Instructions
```

````

**File name:** `02-langchain-agents-model-integration.md`

Bas dhyan rahe: outer code block ko copy karte waqt **starting aur ending ` ```text ` lines ko file mein mat rakhna**. File ki first line directly `# LangChain: Agents & Model Integration` honi chahiye.
````Haan, sahi pakde 😄 Problem ye hai ki writing block ki wajah se Markdown **render** ho raha tha. Tumhe **raw Markdown content** chahiye jisme `##`, `###`, triple backticks etc. literally dikh rahe hain.

 Isko **direct copy karke `.md` file** mein save karo:

````
# LangChain: Agents & Model Integration

## 1. Load API Keys

Use `.env` to store API keys safely.

```python
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
````

 > **Note:** Make sure the variable name is `OPENAI_API_KEY`, not `OPEN_API_KEY`.

---

 ## 2\. Create an Agent

 An **Agent** allows an LLM to use tools when necessary.

```
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get the weather for this city."""
    return f"The weather of {city} is sunny"

agent = create_agent(
    model="gpt-5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)
```

 ### Invoke the Agent

```
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

 ### Remember

 > **Agent = LLM + Tools + Instructions**

---

 ## 3\. Using Different Models

 LangChain provides `init_chat_model()` to initialize different chat models.

```
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1")

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 ## 4\. OpenAI

 ### Using `init_chat_model()`

```
model = init_chat_model("gpt-4.1")
```

 ### Using `ChatOpenAI`

```
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1")

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 ## 5\. Google Gemini

 ### Using `init_chat_model()`

```
model = init_chat_model(
    "google_genai:gemini-2.5-flash-lite"
)
```

 ### Using `ChatGoogleGenerativeAI`

```
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 ## 6\. Groq

```
from langchain_groq import ChatGroq

model = ChatGroq(
    model="qwen/qwen3-32b"
)

response = model.invoke("Hello, how are you?")
print(response.content)
```

---

 # Quick Revision

```
.env
  ↓
API Keys
  ↓
LangChain Model
  ↓
invoke()
  ↓
Response
```

 ## Main Concepts

 - **OpenAI** → `ChatOpenAI`
- **Google Gemini** → `ChatGoogleGenerativeAI`
- **Groq** → `ChatGroq`
- **Generic model initialization** → `init_chat_model()`
- **Agent** → Model + Tools + System Instructions
- **invoke()** → Send input and get a complete response

 ## Easy Memory Trick

```
invoke()  → One input → Complete response

stream()  → One input → Chunks of response

batch()   → Multiple inputs → Multiple responses

Agent     → Model + Tools + Instructions
```



Bas dhyan rahe: outer code block ko copy karte waqt **starting aur ending ` ```text ` lines ko file mein mat rakhna**. File ki first line directly `# LangChain: Agents & Model Integration` honi chahiye.
````
