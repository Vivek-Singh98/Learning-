LangChain: Streaming and Batch
1. Streaming
What is Streaming?

Streaming in LangChain allows us to receive the model's output incrementally instead of waiting for the complete response.

The output can arrive chunk-by-chunk (often token-by-token or in small pieces), allowing us to display the response while the model is still generating it.

Simple idea

Without streaming:

User → Model → Wait → Complete response


With streaming:

User → Model → Chunk 1 → Chunk 2 → Chunk 3 → ... → Complete response


So, streaming is useful when we want to give the user immediate feedback instead of making them wait for the entire response.

Example
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini"
)

for chunk in model.stream("Write a 200-word paragraph about AI"):
    print(chunk.content, end="", flush=True)

Important points

model.stream() starts a streaming request.

The model does not return the entire response at once.

We receive multiple chunks.

chunk.content contains the text from the current chunk.

end="" prevents Python from adding a new line after every chunk.

flush=True makes the output appear immediately in the terminal.

Why use Streaming?

Streaming is useful for:

Chat applications

AI assistants

Long responses

Agent applications

Improving perceived response speed

Showing users that the model is actively generating a response

Remember

Streaming = Get the response piece-by-piece.

2. Batch
What is Batch?

Batch in LangChain is used when we have multiple independent inputs that we want to send to the model.

Instead of calling the model separately for every input:

model.invoke("question 1")
model.invoke("question 2")
model.invoke("question 3")


we can use:

model.batch([
    "question 1",
    "question 2",
    "question 3"
])


LangChain can process these independent inputs concurrently, which can make processing multiple requests more efficient.

Example
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

Understanding max_concurrency
config={
    "max_concurrency": 5
}


max_concurrency controls how many batch tasks can be executed concurrently.

For example:

max_concurrency = 1
    ↓
Process one task at a time

max_concurrency = 5
    ↓
Up to 5 tasks can run concurrently


It is a concurrency limit, not a guarantee that exactly 5 requests will always run at the same time.

Important points

model.batch() accepts a list of inputs.

Each input is treated as an independent request.

It returns a list of responses.

The response at each position corresponds to the input at the same position.

max_concurrency can be used to control concurrent execution.

Example

Input:

[
    "Why do parrots talk?",
    "Why do airplanes fly?",
    "What is AI?"
]


Output:

Response to: Why do parrots talk?
Response to: Why do airplanes fly?
Response to: What is AI?

Remember

Batch = Send/process multiple independent inputs together.

3. Streaming vs Batch
Feature	Streaming	Batch
Main purpose	Receive output incrementally	Process multiple inputs
Method	stream()	batch()
Input	Usually one input	Multiple inputs
Output	Chunks	List of responses
Useful for	Chat/UI responses	Multiple independent requests
Key idea	Response arrives piece-by-piece	Multiple requests are processed
4. Quick Memory Trick
invoke()
model.invoke(input)


One input → One complete response

stream()
model.stream(input)


One input → Many chunks

batch()
model.batch([input1, input2, input3])


Many inputs → Many complete responses

5. Easy Way to Remember
invoke()
    ↓
ONE input
    ↓
ONE complete response


stream()
    ↓
ONE input
    ↓
MANY chunks
    ↓
ONE complete response


batch()
    ↓
MANY inputs
    ↓
MANY responses

Final takeaway

Invoke = Give me the complete answer.

Stream = Give me the answer as it is generated.

Batch = Process multiple independent inputs.
