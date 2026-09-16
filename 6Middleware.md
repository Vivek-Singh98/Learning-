 # 1\. What is Middleware?

 **Middleware provides a way to more tightly control what happens inside an agent.**

 An agent normally follows a flow such as:

```
User Request
     ↓
   Model
     ↓
   Tool
     ↓
   Model
     ↓
  Result
```

 With middleware, we can intercept and control different stages of the agent execution:

```
User Request
     ↓
 Middleware
     ↓
   Model
     ↓
 Middleware
     ↓
   Tool
     ↓
   Model
     ↓
 Middleware
     ↓
  Result
```

 Middleware acts like a **control layer around the agent's execution**.

---

 # 2\. Why Do We Need Middleware?

 Middleware is useful when we need additional control over agent behavior.

 Common use cases include:

 - **Logging and monitoring**
  - Track agent behavior
  - Store execution information
  - Debug agent failures
  - Collect analytics
- **Prompt transformation**
  - Modify or enrich prompts before they reach the model
  - Add system instructions
  - Inject contextual information
- **Tool control**
  - Control which tools the agent can use
  - Restrict dangerous tools
  - Add validation before tool execution
- **Output formatting**
  - Transform or validate model output
  - Ensure a particular response format
- **Retries**
  - Retry failed model calls
  - Retry failed tool calls
- **Fallbacks**
  - Use another model when the primary model fails
  - Provide alternative execution paths
- **Early termination**
  - Stop an agent when a specific condition is met
  - Prevent unnecessary model/tool calls
- **Rate limiting**
  - Control how frequently models or tools can be called
- **Guardrails**
  - Validate inputs and outputs
  - Prevent unsafe operations
- **PII detection**
  - Detect Personally Identifiable Information
  - Prevent sensitive information from being exposed or processed incorrectly
- **Human-in-the-loop**
  - Pause an agent before sensitive operations
  - Ask a human for approval

---

 # 3\. Airport Security Analogy

 A useful way to understand middleware is to compare an agent with an airport.

 ### Airport

```
Passenger
    ↓
Security Check
    ↓
Immigration
    ↓
Boarding
    ↓
Flight
```

 Each checkpoint controls what happens before the passenger moves forward.

 Middleware works similarly:

```
Request
   ↓
Middleware 1
   ↓
Model
   ↓
Middleware 2
   ↓
Tool
   ↓
Middleware 3
   ↓
Model
   ↓
Middleware 4
   ↓
Result
```

 Each middleware can inspect, modify, approve, reject, retry, or stop an operation.

 ### Interview explanation

 > "Middleware acts as a control layer around an agent. It allows us to intercept model and tool execution so that we can implement logging, retries, guardrails, human approval, rate limiting, summarization, and other runtime behaviors."

---

 # 4\. Common Agent Middleware Use Cases

 Some common middleware patterns are:

```
1. Summarization Middleware
2. Human-in-the-Loop Middleware
3. Model Call Limit
4. Model Fallback
5. PII Detection
6. Tool Retry
7. Model Retry
8. Guardrails
9. Logging / Analytics
10. Rate Limiting
```

---

 # 5\. Summarization Middleware

 Long conversations can become expensive because every new model call may need to process a large message history.

 For example:

```
Message 1
Message 2
Message 3
Message 4
Message 5
...
Message 100
```

 Sending all 100 messages to the model repeatedly can increase:

 - Token usage
- Latency
- Cost
- Context-window pressure

 **Summarization Middleware** helps solve this problem.

 It can summarize older messages and retain only the important information.

 Conceptually:

```
Before:

Message 1
Message 2
Message 3
...
Message 10
Message 11
Message 12

             ↓
      Summarization
             ↓

Summary of older messages
Message 9
Message 10
Message 11
Message 12
```

 The agent can then continue with a much smaller context.

---

 # 6\. Message-Based Summarization

 A summarization middleware can be configured to trigger after a particular number of messages.

 For example:

```
trigger=("messages", 10)
```

 This means the summarization process can be triggered when the message count reaches the configured threshold.

 We can also configure how many messages should remain after summarization.

 For example:

```
keep=("messages", 4)
```

 Conceptually:

```
10+ messages
      ↓
Summarization
      ↓
Summary + latest 4 messages
```

 The exact behavior depends on the middleware/version being used.

---

 # 7\. Summarization Middleware Example

```
import os

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Make sure the API key is available to the SDK.
# The OpenAI SDK normally expects OPENAI_API_KEY.
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Create an in-memory checkpointer
checkpointer = InMemorySaver()

# Create agent with summarization middleware
agent = create_agent(
    model="gpt-4o-mini",
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("messages", 10),
            keep=("messages", 4),
        )
    ],
)

# Thread ID allows the agent to maintain conversation state
config = {
    "configurable": {
        "thread_id": "test-1"
    }
}

questions = [
    "What is 2 + 2?",
    "What is 2 + 5?",
    "What is 2 + 8?",
    "What is 2 + 3?",
    "What is 2 + 44?",
]

for question in questions:
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config,
    )

    print(result)
```

---

 # 8\. Why Do We Need a Thread ID?

 When using a checkpointer, conversations need an identifier so the framework knows which state belongs to which conversation.

 Example:

```
config = {
    "configurable": {
        "thread_id": "test-1"
    }
}
```

 Think of `thread_id` as a **conversation ID**.

 For example:

```
thread_id = "user-123-chat-1"
```

 The checkpointer can use that ID to store and retrieve the state associated with the conversation.

---

 # 9\. Token-Based Summarization

 Message count is not the only way to decide when to summarize.

 A conversation might contain:

```
5 messages
```

 but each message could be extremely large.

 Therefore, token-based summarization can be more useful when the main concern is context size.

 Conceptually:

```
Messages
   ↓
Token Counter
   ↓
Token limit exceeded?
   ↓
Yes
   ↓
Summarize older context
   ↓
Continue execution
```

 The important interview point is:

 > "Message count and token count are different. Ten short messages may use fewer tokens than two very large messages."

---

 # 10\. Human-in-the-Loop

 ## Definition

 **Human-in-the-loop (HITL)** means that an autonomous agent can pause and request human intervention before performing a sensitive or important action.

 Without HITL:

```
User
  ↓
Agent
  ↓
Tool
  ↓
Action
  ↓
Result
```

 With HITL:

```
User
  ↓
Agent
  ↓
Tool Request
  ↓
Human Approval
  ↓
Approved?
 ┌───────┴───────┐
Yes              No
 ↓                ↓
Tool             Stop
 ↓
Result
```

---

 # 11\. Why Do We Need Human-in-the-Loop?

 Some operations have real-world consequences.

 Examples:

 - Sending an email
- Making a financial transaction
- Purchasing something
- Deleting data
- Updating production infrastructure
- Publishing content
- Changing customer information
- Executing sensitive tools

 For these operations, allowing an agent to act completely autonomously can be risky.

 HITL gives a human the opportunity to review the action before it happens.

---

 # 12\. Example: Email Agent

 Imagine an agent has two tools:

```
read_email()
send_email()
```

 Reading an email is generally a read-only operation.

 Sending an email is an external side effect.

 Therefore, we may want:

```
read_email → automatic
send_email → human approval required
```

 Architecture:

```
User
  ↓
Agent
  ↓
Need to send email
  ↓
Human Approval
  ↓
 ┌───────────────┐
 │               │
Approve        Reject
 │               │
 ↓               ↓
send_email     Stop
```

---

 # 13\. Human-in-the-Loop Example

```
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

# -----------------------------
# Tools
# -----------------------------

def read_email(email_id: str) -> str:
    """Read an email."""
    return f"Email content for ID: {email_id}"

def send_email(
    recipient: str,
    subject: str,
    body: str,
) -> str:
    """Send an email."""
    return (
        f"Email sent successfully to {recipient}. "
        f"Subject: {subject}"
    )

# -----------------------------
# Checkpointer
# -----------------------------

checkpointer = InMemorySaver()

# -----------------------------
# Agent
# -----------------------------

agent = create_agent(
    model="gpt-4o",
    tools=[
        read_email,
        send_email,
    ],
    checkpointer=checkpointer,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": [
                        "approve",
                        "reject",
                        "edit",
                    ]
                },
                "read_email": False,
            }
        )
    ],
)

# -----------------------------
# Thread configuration
# -----------------------------

config = {
    "configurable": {
        "thread_id": "email-thread-1"
    }
}

# -----------------------------
# User request
# -----------------------------

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Send an email to John saying "
                    "'Hi, how are you?'"
                )
            )
        ]
    },
    config,
)

print(result)
```

 > **Note:** Middleware APIs can vary between LangChain/LangGraph releases. If an example gives an import or parameter error, check the version-specific documentation for the installed package version.

---

 # 14\. What Happens When the Agent Is Interrupted?

 The important concept is that the agent does **not** simply continue executing the sensitive operation.

 Instead:

```
User Request
     ↓
Agent
     ↓
send_email()
     ↓
HITL Middleware
     ↓
INTERRUPT
     ↓
Human reviews action
```

 The human can then make a decision.

 Possible decisions include:

```
approve
reject
edit
```

---

 # 15\. Approval Flow

 Conceptually:

```
result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="Send an email to John saying hello."
            )
        ]
    },
    config,
)
```

 The agent may reach:

```
send_email(...)
```

 The middleware pauses execution.

 The application can inspect the interrupt information:

```
print(result)
```

 Then the human decides whether the action should proceed.

 The agent can subsequently be resumed using the framework's interrupt/resume mechanism for the installed LangGraph version.

---

 # 16\. Why Is a Checkpointer Important for HITL?

 A human approval step means the agent's execution can be paused.

 Therefore, the system needs to preserve state.

 For example:

```
Step 1 → Agent receives request
Step 2 → Agent decides to send email
Step 3 → INTERRUPT
Step 4 → Human thinks/reviews
Step 5 → Agent resumes
Step 6 → Email is sent
```

 The checkpointer helps maintain the state between these steps.

```
checkpointer = InMemorySaver()
```

 For production systems, a persistent checkpointer/database is generally preferable to in-memory storage.

---

 # 17\. Middleware + HITL

 Middleware and HITL work very well together.

 For example:

```
                 Agent
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
   Logging      Guardrail    Retry
       │           │           │
       └───────────┼───────────┘
                   ↓
                Tool
                   ↓
             HITL Check
                   ↓
          Human Approval
                   ↓
                Action
```

 This allows us to build safer and more observable agents.

---

 # 18\. Other Useful Middleware Patterns

 ## 18.1 Model Retry

 A model call can fail because of:

 - Temporary API errors
- Network problems
- Rate limits
- Service availability issues

 A retry middleware/pattern can retry the model call.

```
Model Call
    ↓
Failed?
    ↓
Retry
    ↓
Retry
    ↓
Success
```

---

 # 19\. Tool Retry

 Tools can also fail.

 For example:

```
Agent
  ↓
API Tool
  ↓
Timeout
  ↓
Retry
  ↓
API Tool
  ↓
Success
```

 Tool retry logic is especially useful for transient failures.

 However, retries should be designed carefully for tools with side effects.

 For example, blindly retrying:

```
send_payment()
```

 could potentially create duplicate transactions.

 For side-effecting tools, idempotency and transaction safety are important.

---

 # 20\. Model Fallback

 Suppose the primary model is unavailable.

 We can design a fallback:

```
Primary Model
      ↓
    Failed
      ↓
Fallback Model
      ↓
    Result
```

 For example:

```
GPT-4o
  ↓ failure
Fallback model
  ↓
Result
```

 This improves system resilience.

---

 # 21\. Model Call Limit

 An agent can sometimes enter an unexpected loop:

```
Model
 ↓
Tool
 ↓
Model
 ↓
Tool
 ↓
Model
 ↓
Tool
 ↓
...
```

 A model-call limit can protect the application.

 For example:

```
Maximum model calls = 10

Call 1
Call 2
Call 3
...
Call 10
 ↓
Stop execution
```

 This helps control:

 - Cost
- Latency
- Infinite loops
- Unexpected agent behavior

---

 # 22\. PII Detection

 PII means **Personally Identifiable Information**.

 Examples include:

 - Email addresses
- Phone numbers
- Home addresses
- Government identifiers
- Other sensitive identifying information

 A PII middleware can inspect data before it reaches a model or external tool.

 Conceptually:

```
User Input
    ↓
PII Detection
    ↓
PII found?
 ┌───────┴───────┐
Yes              No
 ↓                ↓
Mask/Block       Model
```

 Example:

```
Original:

"My phone number is 9876543210"

After masking:

"My phone number is **********"
```

 The exact behavior depends on the application's privacy requirements.

---

 # 23\. Guardrails

 Guardrails enforce rules around agent behavior.

 For example:

```
Agent wants to delete a customer
             ↓
        Guardrail
             ↓
Is deletion allowed?
       ↓           ↓
     Yes           No
      ↓             ↓
   Continue        Stop
```

 Guardrails can validate:

 - User input
- Tool arguments
- Model output
- Business rules
- Security policies

---

 # 24\. Logging and Analytics

 Middleware can also observe the execution.

 Example:

```
Request
   ↓
Logging Middleware
   ↓
Model
   ↓
Logging Middleware
   ↓
Tool
   ↓
Logging Middleware
   ↓
Result
```

 We can collect information such as:

```
- Model used
- Number of model calls
- Number of tool calls
- Execution time
- Errors
- Retry count
- Token usage
- Tool execution status
```

 This is very useful when debugging production agents.

---

 # 25\. Complete Conceptual Architecture

 A production agent might look like:

```
                    User Request
                         │
                         ↓
                ┌─────────────────┐
                │ Input Middleware│
                │  - PII          │
                │  - Guardrails   │
                └────────┬────────┘
                         ↓
                      Model
                         │
                         ↓
                ┌─────────────────┐
                │ Model Middleware│
                │  - Retry        │
                │  - Rate Limit   │
                │  - Logging      │
                └────────┬────────┘
                         ↓
                    Tool Call
                         │
                         ↓
                ┌─────────────────┐
                │ Tool Middleware │
                │  - Validation   │
                │  - Retry        │
                │  - HITL         │
                └────────┬────────┘
                         ↓
                     Tool
                         │
                         ↓
                      Model
                         │
                         ↓
                ┌─────────────────┐
                │ Output Middleware│
                │  - Validation   │
                │  - Formatting   │
                └────────┬────────┘
                         ↓
                       Result
```

---

 # 26\. Middleware vs Tool

 These are different concepts.

 ### Tool

 A **tool performs an action**.

 Examples:

```
search_web()
read_email()
send_email()
get_weather()
query_database()
```

 ### Middleware

 **Middleware controls or observes the execution of the agent/tool/model.**

 Examples:

```
Logging
Retry
Guardrails
Human approval
Rate limiting
Summarization
PII detection
```

 A simple way to remember:

 > **Tool = performs the work.**

 > **Middleware = controls/observes how the work is performed.**

---

 # 27\. Middleware vs Agent

 An agent decides what action should be taken.

```
User
 ↓
Agent
 ↓
"I should call send_email"
 ↓
send_email()
```

 Middleware can intervene around this process:

```
User
 ↓
Agent
 ↓
Middleware
 ↓
send_email()
 ↓
Middleware
 ↓
Result
```

 So:

 > **Agent = decision maker**

 > **Middleware = control/observation layer**

 > **Tool = action executor**

---

 # 28\. Important Interview Question

 ## Q: Why would you use middleware instead of putting everything inside the agent prompt?

 ### Answer

 Middleware provides programmatic control over execution.

 A prompt can tell an agent:

 > "Always ask for approval before sending an email."

 But relying only on a prompt is weaker than enforcing the rule at the execution layer.

 Middleware can actually intercept the tool call and pause execution.

```
Prompt instruction
       ↓
Agent decision
       ↓
Middleware enforcement
       ↓
Tool execution
```

 This is particularly important for security-sensitive and side-effecting operations.

---

 # 29\. Interview Questions & Answers

 ## Q1. What is middleware in an agent system?

 **Answer:**

 > Middleware is a control layer that intercepts or observes agent execution. It allows us to implement features such as logging, retries, fallbacks, guardrails, rate limiting, summarization, PII detection, and human approval without putting all of that logic directly into the agent's core behavior.

---

 ## Q2. Why is middleware useful?

 **Answer:**

 > Middleware separates cross-cutting concerns from the agent's main reasoning logic. For example, instead of adding retry or logging code to every agent, we can implement it as middleware and apply it consistently.

---

 ## Q3. What is Summarization Middleware?

 **Answer:**

 > Summarization middleware reduces conversation context by summarizing older messages when the configured threshold is reached. This can help control token usage and context size while preserving important information from the conversation.

---

 ## Q4. Why do we need summarization?

 **Answer:**

 > Long conversations increase token usage, latency, and context-window pressure. Summarization compresses older conversation history into a smaller representation while keeping recent messages available.

---

 ## Q5. What is Human-in-the-Loop?

 **Answer:**

 > Human-in-the-loop means the agent can pause before performing a sensitive operation and request a human decision. The human can approve, reject, or potentially modify the proposed action, depending on the workflow.

---

 ## Q6. Give an example of HITL.

 **Answer:**

 > Suppose an agent can send emails. Reading emails may be allowed automatically, but sending an email can require human approval. The middleware intercepts the `send_email` tool call, pauses the agent, and waits for the human decision before allowing the action to continue.

---

 ## Q7. Why is a checkpointer important for HITL?

 **Answer:**

 > HITL can pause an agent between steps. A checkpointer stores the agent state so execution can later resume from the correct point after the human provides a decision.

---

 ## Q8. What is the difference between retry and fallback?

 **Retry:**

```
Same operation
     ↓
Retry
     ↓
Retry
     ↓
Success
```

 **Fallback:**

```
Primary implementation
       ↓
     Failure
       ↓
Alternative implementation
       ↓
     Success
```

 A retry repeats the same operation, while a fallback switches to an alternative model, service, or strategy.

---

 ## Q9. Why do we need a model-call limit?

 **Answer:**

 > Agents can sometimes make too many model calls because of loops or unexpected reasoning paths. A model-call limit prevents excessive execution and helps control cost, latency, and runaway behavior.

---

 ## Q10. Why should tool retries be handled carefully?

 **Answer:**

 > Some tools have side effects. Retrying a read-only API call may be safe, but retrying an operation such as sending money or creating an order can cause duplicate actions unless the operation is designed to be idempotent.

---

 # 30\. One-Minute Interview Explanation

 If the interviewer asks:

 > **"Explain middleware in an agent."**

 You can say:

 > "Middleware is a control layer around an agent that allows us to intercept and manage model and tool execution. Without middleware, the flow is basically request, model, tool, model, and result. With middleware, we can add cross-cutting functionality such as logging, retries, fallbacks, guardrails, rate limiting, PII detection, summarization, and human approval.
>
>  For example, if an agent has a `send_email` tool, I can use Human-in-the-Loop middleware to pause execution before the email is sent. The human can approve, reject, or edit the action, and then the agent can resume from the saved state.
>
>  Another example is Summarization Middleware. If the conversation becomes too large, the middleware can summarize older messages and keep the recent messages, which helps control context size, latency, and token usage.
>
>  So, in simple terms: the agent makes decisions, tools perform actions, and middleware provides control and safety around the execution."

---

 # 31\. Quick Revision

```
Middleware
    ↓
Control layer around agent execution

Common uses:
    ↓
Logging
Retries
Fallbacks
Guardrails
Rate limiting
PII detection
Summarization
Human approval
Output validation
Tool control
```

 ### Remember these three concepts

```
AGENT
  ↓
Decides what to do

MIDDLEWARE
  ↓
Controls / observes execution

TOOL
  ↓
Performs an action
```

 ### HITL

```
Agent
  ↓
Sensitive action
  ↓
Human approval
  ↓
Approve → Continue
Reject  → Stop
Edit    → Modify and continue
```

 ### Summarization

```
Large conversation
       ↓
Summarization
       ↓
Compressed history
+
Recent messages
       ↓
Smaller context
```

---

 # 32\. Final Takeaway

 The main idea behind middleware is **separation of concerns**.

 Instead of putting every requirement into the agent itself:

```
Agent
 ├── Logging
 ├── Retry
 ├── Guardrails
 ├── PII detection
 ├── Human approval
 ├── Rate limiting
 ├── Summarization
 └── Business logic
```

 we can separate these concerns:

```
                  Agent
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
    Middleware Layer        Tools
          │
    ┌─────┼─────┬─────┬─────┐
    ↓     ↓     ↓     ↓     ↓
 Logging Retry  HITL  PII  Guardrails
```

 This makes agent applications easier to:

 - Maintain
- Debug
- Secure
- Test
- Scale
- Monitor
- Control

 **Core interview statement:**

 > **"Middleware gives us a programmatic control layer around an agent's model and tool execution, allowing us to add cross-cutting concerns such as observability, reliability, safety, context management, and human approval without tightly coupling those concerns to the agent's core logic."**

 This version is suitable to save directly as **`README.md`**. I also deliberately kept the code focused on the concepts while flagging the places where LangChain/LangGraph APIs can differ by installed version.
