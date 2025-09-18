"""
LangChain Pipelines (LCEL) – minimal, runnable examples.

This file shows how to build two kinds of pipelines using the LangChain Expression
Language (LCEL):

1) Linear pipeline (prompt → model → parser)
2) Parallel/branched pipeline (one input → multiple computations in parallel)
"""

from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI


def build_linear_pipeline(model_name: str = "gpt-4o-mini"):
    """Create a simple LCEL pipeline: prompt → model → string output.

    Input schema: {"topic": str}
    Output: str
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise assistant."),
        (
            "human",
            "Write a two-sentence overview about {topic}. Keep it clear and direct.",
        ),
    ])

    # Component 1 - LLM
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Component 2 - Parser (to parse the output)
    parser = StrOutputParser()

    # LCEL uses the | operator to compose runnables
    chain = prompt | llm | parser
    return chain


def build_parallel_pipeline(model_name: str = "gpt-4o-mini"):
    """Create a branched pipeline that runs computations in parallel.

    The branches:
      - "summary": Generate a brief description about the topic
      - "tags": Generate 3 comma-separated tags

    Input schema: {"topic": str}
    Output: {"summary": str, "tags": str}
    """
    # Component 1 - Prompt
    base_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise assistant."),
        ("human", "{instruction} about {topic}"),
    ])

    # Component 2 - LLM
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Component 3 - Parser (to parse the output)
    parser = StrOutputParser()

    # Each branch is its own small pipeline that shares the same LLM
    summary_branch = (
        base_prompt.partial(instruction="Give a 2-sentence overview") | llm | parser
    )

    # Component 4 - Parser (to parse the output)
    tags_branch = (
        base_prompt.partial(instruction="Provide 3 topical tags, comma-separated")
        | llm
        | parser
        | RunnableLambda(lambda s: s.replace(" ", ""))  # normalize spacing in tags
    )

    # RunnableParallel runs all branches and returns a dict of their outputs
    parallel = RunnableParallel(summary=summary_branch, tags=tags_branch)
    return parallel


def run_linear_example() -> str:
    """Run the linear pipeline with a sample input and return the result."""
    chain = build_linear_pipeline()
    return chain.invoke({"topic": "LangChain pipelines (LCEL)"})


def run_parallel_example() -> Dict[str, Any]:
    """Run the parallel pipeline with a sample input and return the result."""
    chain = build_parallel_pipeline()
    return chain.invoke({"topic": "LangChain pipelines (LCEL)"})


if __name__ == "__main__":
    print("— Linear pipeline —")
    try:
        linear_output = run_linear_example()
        print(linear_output)
    except Exception as exc:  # pragma: no cover
        print(f"Linear pipeline failed: {exc}")
    print("--------------------------------\n")


    print("\n— Parallel pipeline —")
    try:
        parallel_output = run_parallel_example()
        print(parallel_output)
    except Exception as exc:  # pragma: no cover
        print(f"Parallel pipeline failed: {exc}")


