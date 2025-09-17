from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools, initialize_agent, AgentType

def langchain_agent():
    llm = OpenAI(temperature=0.5)

    # Load tools for the agent to use
    tools = load_tools(["wikipedia", "llm-math"],  # Specify the tools you want to use
                       llm=llm)  # Pass the llm to tools that need it

    # Initialize the agent with the tools and LLM
    agent = initialize_agent(tools,  # tools the agent can use
                             llm,  # the language model
                             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # type of agent.
                             verbose=True)

    # Run the agent with a specific query
    result = agent.run(
        "What is the average age of a dog? Find the number, the average age, and at last, multiply it by 3"
    )


if __name__ == "__main__":
    print("Running script...\n")

    age = langchain_agent()

    print(age)
