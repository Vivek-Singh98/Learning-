#Streaming and Batch 
#Streaming :"In LangChain, streaming is a method that allows developers to receive and display outputs 
#            from large language models (LLMs) and complex agent chains incrementally,chunk-by-chunk or 
#            token-by-token, instead of waiting for the entire response to be generated"

from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini"
)

for chunk in model.stream("write a 200 word paragrapgh in AI"):
    print(chunk.text, end="|", flush=True)

#streaming is simple we dont wait for whole paragraph we it generate line by line 


#Bath : In LangChain, batch is a built-in method on Runnable objects used to process multiple 
#       independent inputs in parallel

responses = model.batch([
    "why parrot talk",
    "why airplan fly",
    "what is AI"
],
config={
    'max_concurrency':5, #Limit 5 parrel call
})

for response in responses:
    print(response)

