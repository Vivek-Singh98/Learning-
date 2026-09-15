import os 
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv(("GOOGLE_API_KEY"))
os.environ["GROQ_API_KEY"] = os.getenv(("GROQ_API_KEY"))

from langchain.agents import create_agent 
#version :  "1.1.0""


#act as a tool for our LLM 
def get_weather(city:str)->str:
    """ Get the weather for this city """
    return f"The weather of this {city} is sunny"


agent = create_agent(
    model ="gpt5",
    tools =[get_weather],
    system_prompts ="you are helpful assistance"
)

agent,invoke({"messages":[{"role":"user","content":"What is weather in dehradun"}]})

response["messages"][-1].content


#Model Integration with OpenAI , Google Gemini and GROQ 

from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-4.1")
print(model)

##Invoke The Model 
response = model.invoke("Hello How are you ")
print(response.content)


#How to call a Google gemine model 
from langchain.chat_models import init_chat_model 
model = init_chat_model("google_genai : gemini-2.5-flash-lite")
response = model.invoke("why do parrot talk")
print(response.content)


# we can use ChatOpenAI insied of init_chat_model
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model ="gpt-4.1")
response = model.invoke("hello how are you ?")
print(response.content)


# same for Gemine AI chatbot 

from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model =" gemini-2.5-flash-lite")
response = model.invoke("hello how are you ?")
print(response.content)


##Groq Model Integration 

from langchain_groq import ChatGroq
model = ChatGroq(model ="qwen/qwen3-32b")
response = model.invoke("hello how are you ?")
print(response.content)







