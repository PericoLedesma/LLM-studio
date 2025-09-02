from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize the LLM (using OpenAI API under the hood)
llm = ChatOpenAI(model="gpt-4o-mini")  # replace with your model of choice

# 2. Create a simple prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{question}")
])

# 3. Format the prompt with user input
chain = prompt | llm  # Pipeline: prompt → model

# 4. Run inference
response = chain.invoke({"question": "What is the capital of Spain?"})

print(response.content)