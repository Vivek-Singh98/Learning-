# TOOLS :
# An LLM tool is a registered function or external API that a large language model can call
# to interact with real-world systems, fetch live data, or perform actions beyond text generation
with tool + bind_tool()

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Load variables from .env
load_dotenv()

# Create the LLM
model = ChatOpenAI(
    model="gpt-4o-mini"
)


# Create a tool
@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"The weather in {location} is sunny."


# Give the tool to the LLM
model_with_tools = model.bind_tools([get_weather])

# Ask the LLM a question
response = model_with_tools.invoke(
    "What is the weather in Boston?"
)

# Print the LLM response
print(response.content)


# 2. Using create_agent()
# This is simpler when you want the LLM to automatically call the tool and use its result.

from dotenv import load_dotenv
from langchain.agents import create_agent

# Load .env file
load_dotenv()


# Create a tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny."


# Create an agent and give it the tool
agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant."
)


# Ask the agent a question
response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the weather in Dehradun?"
        }
    ]
})


# Print the final answer
print(response["messages"][-1].content)

# Check if the LLM requested any tools
for tool_call in response.tool_calls:
    print("Tool name:", tool_call["name"])
    print("Tool arguments:", tool_call["args"])
