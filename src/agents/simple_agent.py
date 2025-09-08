from pydantic import  BaseModel
from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate # For prompt templates
from langchain_core.output_parsers import PydanticOutputParser # For output parsing, meaning we can define the output format using Pydantic models
# from langchain_core.agents import create_tool_calling_agent, AgentExecutor # For creating agents
from langchain.agents import create_tool_calling_agent, AgentExecutor



import os
openai_api_key = os.environ.get("OPENAI_API_KEY")
# anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY") #TODO


class ResearchResponse(BaseModel):
    topic: str
    summery: str
    sources: list[str]
    tool_used: list[str]


llm = ChatOpenAI(model_name="gpt-4",
                 temperature=0)
# llm = ChatAnthropic(model="claude-2", temperature=0)

# response = llm.invoke("Whats the meaning of life?")
# print(response)


parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """
         You are a research assistant that will help generate a research paper.
         Answer the user query and use necessary tools.
         Wrap the output in this format and provide no other text\n{format_instructions}
         """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent= create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[],
)


agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
raw_responser = agent_executor.invoke({"query": "Write a short research paper on the impact of climate change on "
                                                "marine biodiversity."})

# print(raw_responser)
try:
    structure_response = parser.parse(raw_responser.get("output")[0]["text"])
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_responser)

print(structure_response)  # .topic