from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model='llama3')

messages = [
    ('system', 'You are a sentiment analysis model that only outputs the sentiment of my input'),
    ('user', '{input}')
]

prompt = ChatPromptTemplate.from_messages(messages)

chain = prompt | llm | StrOutputParser()

input = "The course is very inconsistent, it repeats the same one minute in all of the videos, when reviewing the dataframe. Many times some things are asked without providing previous explanation, and the final assignment is also an example, I had to search all over internet to resolve it, because I couldn't find any reference in the content provided."

print(chain.invoke({'input': input}))