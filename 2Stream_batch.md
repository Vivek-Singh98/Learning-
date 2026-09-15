````
# LangChain: Streaming and Batch

## 1. Streaming

### What is Streaming?

Streaming in LangChain allows us to receive the model's output **incrementally** instead of waiting for the complete response.

The output arrives **chunk-by-chunk**, allowing us to display the response while the model is still generating it.

### Simple Idea

**Without Streaming:**

```text
User → Model → Wait → Complete Response
````

 **With Streaming:**

```
User → Model → Chunk 1 → Chunk 2 → Chunk 3 → ... → Complete Response
```

 > **Streaming = Get the response piece-by-piece.**

 ### Example

```
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini"
)

for chunk in model.stream("Write a 200-word paragraph about AI"):
    print(chunk.content, end="", flush=True)
```

 ### Important Points

 - `model.stream()` starts a streaming request.
- The complete response is not returned at once.
- We receive multiple chunks.
- `chunk.content` contains the text from the current chunk.
- `end=""` prevents a new line after every chunk.
- `flush=True` makes the output appear immediately.

 ### Why Use Streaming?

 Streaming is useful for:

 - Chat applications
- AI assistants
- Long responses
- Agent applications
- Improving perceived response speed
- Showing users that the model is actively generating

 ### Remember

 > **Streaming = Response piece-by-piece**

---

 ## 2\. Batch

 ### What is Batch?

 Batch in LangChain is used when we have **multiple independent inputs** that we want to send to the model.

 Instead of calling the model separately:

```
model.invoke("question 1")
model.invoke("question 2")
model.invoke("question 3")
```

 We can use:

```
model.batch([
    "question 1",
    "question 2",
    "question 3"
])
```

 LangChain can process these independent inputs concurrently.

 > **Batch = Process multiple independent inputs.**

 ### Example

```
responses = model.batch(
    [
        "Why do parrots talk?",
        "Why do airplanes fly?",
        "What is AI?"
    ],
    config={
        "max_concurrency": 5
    }
)

for response in responses:
    print(response.content)
```

---

 ## 3\. Understanding `max_concurrency`

```
config={
    "max_concurrency": 5
}
```

 `max_concurrency` controls how many batch tasks can run concurrently.

 ### Example

```
max_concurrency = 1
        ↓
One task at a time

max_concurrency = 5
        ↓
Up to 5 tasks can run concurrently
```

 > `max_concurrency` is a limit, not a guarantee that exactly 5 tasks will always run at the same time.

 ### Important Points

 - `model.batch()` accepts multiple inputs.
- Each input is treated as an independent request.
- It returns a list of responses.
- Responses correspond to the inputs in the same order.
- `max_concurrency` controls concurrent execution.

 ### Example Input

```
[
    "Why do parrots talk?",
    "Why do airplanes fly?",
    "What is AI?"
]
```

 ### Example Output

```
Response to: Why do parrots talk?
Response to: Why do airplanes fly?
Response to: What is AI?
```

---

 ## 4\. Streaming vs Batch

 | Feature | Streaming | Batch |
| --- | --- | --- |
| Main Purpose | Receive output incrementally | Process multiple inputs |
| Method | `stream()` | `batch()` |
| Input | Usually one input | Multiple inputs |
| Output | Chunks | List of responses |
| Useful For | Chat / UI responses | Multiple independent requests |
| Key Idea | Response arrives piece-by-piece | Multiple requests are processed |

---

 ## 5\. Quick Memory Trick

 ### `invoke()`

```
model.invoke(input)
```

 **One input → One complete response**

 ### `stream()`

```
model.stream(input)
```

 **One input → Many chunks**

 ### `batch()`

```
model.batch([
    input1,
    input2,
    input3
])
```

 **Many inputs → Many complete responses**

---

 ## 6\. Easy Way to Remember

```
invoke()
    ↓
ONE input
    ↓
ONE complete response
```

```
stream()
    ↓
ONE input
    ↓
MANY chunks
    ↓
ONE complete response
```

```
batch()
    ↓
MANY inputs
    ↓
MANY responses
```

---

 ## 7\. Final Takeaway

 > **Invoke** = Give me the complete answer.

 > **Stream** = Give me the answer as it is generated.

 > **Batch** = Process multiple independent inputs.

```

```
