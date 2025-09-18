# Chains vs. Pipelines in LangChain

LangChain provides two main ways to compose LLM-powered workflows: **chains** and **pipelines**. Both help you structure multi-step tasks, but they differ in flexibility, composition, and use cases.

---

## Chains

- **What are they?**  
  Chains are *sequential* workflows: each step takes the output of the previous step as its input.
- **How do they work?**  
  You compose a chain by linking together components (prompts, LLMs, output parsers, etc.) in a fixed order using the `|` operator or by nesting.
- **When to use:**  
  When your workflow is strictly linear (A → B → C), e.g., prompt → LLM → parse output.
- **Limitations:**  
  All steps are run one after another; you can't branch or run steps in parallel.

**Example: Linear Chain**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Components
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Summarize this text in 1 sentence: {text}")
])
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# LCEL chain (linear): prompt -> llm -> parse
chain = prompt | llm | parser

result = chain.invoke({"text": "LangChain makes it easy to build LLM apps."})
print(result)
```

- **Pros:**
  - Simple, readable, and easy to test.
  - Great for deterministic, linear flows (prompting → generation → parsing).
  - Works well with streaming (`.stream()`), batching (`.batch()`), and tooling like tracing.
- **Cons:**
  - No built-in branching or fan-out/fan-in.
  - Parallel execution requires additional components.

---

## Pipelines

- **What are they?**  
  Pipelines represent more flexible workflows that can include branching, parallel steps, and merging. In the LangChain ecosystem, you build these using LCEL primitives like `RunnableParallel`, `RunnableBranch`, `RunnableLambda`, or by defining explicit graphs with LangGraph.
- **How do they work?**  
  Instead of a single linear path, a pipeline can fan-out to multiple sub-computations, run them in parallel, then merge results. You can route inputs based on conditions and compose DAG-like structures.
- **When to use:**  
  When you need conditional logic (route by intent), parallel enrichment (e.g., call multiple tools or retrievers), or multi-stage retrieval/verification (RAG pipelines, multi-agent workflows).
- **Limitations:**  
  More moving parts; higher complexity to design, test, and observe. Requires careful handling of async/parallel behavior and retries.

**Example: Parallel Fan-out/Fan-in Pipeline (LCEL)**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini")
to_str = StrOutputParser()

# Prepare different prompts in parallel (title + summary)
title_prompt = ChatPromptTemplate.from_template(
    "Write a punchy blog post title about: {topic}"
)
summary_prompt = ChatPromptTemplate.from_template(
    "Provide a 2-sentence summary about: {topic}"
)

parallel = RunnableParallel(
    title=(title_prompt | llm | to_str),
    summary=(summary_prompt | llm | to_str),
    original=RunnablePassthrough()
)

# Merge the parallel outputs into a final post outline
combine_prompt = ChatPromptTemplate.from_template(
    """
    Create a short outline for a blog post.
    Title: {title}
    Summary: {summary}
    Topic: {original[topic]}
    """
)

pipeline = parallel | combine_prompt | llm | to_str

result = pipeline.invoke({"topic": "LLM orchestration with LangChain"})
print(result)
```

**Example: Conditional Routing (Branching) with LCEL**
```python
from langchain_core.runnables import RunnableBranch

def is_question(input_dict):
    text = input_dict.get("input", "")
    return text.strip().endswith("?")

qa_prompt = ChatPromptTemplate.from_template(
    "Answer the question concisely: {input}"
)
gen_prompt = ChatPromptTemplate.from_template(
    "Write a short paragraph about: {input}"
)

qa_chain = qa_prompt | llm | to_str
gen_chain = gen_prompt | llm | to_str

routed = RunnableBranch(
    (is_question, qa_chain),  # if question → QA
    gen_chain                 # else → generation
)

print(routed.invoke({"input": "What is RAG?"}))
print(routed.invoke({"input": "RAG systems in production"}))
```

---

## Chains vs. Pipelines: Quick Comparison

| Aspect | Chains | Pipelines |
|---|---|---|
| Structure | Strictly linear | Can branch and merge (DAG-like) |
| Concurrency | Sequential by default | Parallel via `RunnableParallel` |
| Routing | Not built-in | Conditional routing via `RunnableBranch` |
| Complexity | Low | Medium to High |
| Use cases | Prompt → LLM → Parse, simple transforms | RAG, multi-tool enrichment, intent-based routing |
| Observability | Straightforward tracing | Needs good tracing/labels per branch |
| Error handling | Simple retries around the chain | Per-branch retries, fallbacks, timeouts |
| Performance | Adequate for small flows | Better for workloads benefiting from parallelism |

---

## Practical Guidance

- **Start simple with a chain** if your task is linear and stable.
- **Move to a pipeline** when you need any of the following:
  - Fan-out/fan-in parallel steps (e.g., multiple retrievers/tools).
  - Conditional routing (classification → choose a specialized subchain).
  - Multi-stage RAG (retrieve → re-rank → synthesize → verify).
  - Aggregating multiple LLM or tool calls for quality and robustness.
- **Testing tips:**
  - Unit test each component (prompt, parser, retriever) in isolation.
  - Snapshot-test model outputs behind a stable interface.
  - Use `.batch()` for deterministic regression tests on curated inputs.
- **Performance tips:**
  - Prefer `RunnableParallel` to reduce wall-clock time.
  - Use streaming for early tokens when UX matters.
  - Cache stable sub-steps (e.g., deterministic retrieval) where possible.
- **Observability:**
  - Add run names/metadata to critical nodes for better traces.
  - Log branch decisions and timing per sub-step.

---

## Related: LangGraph for Stateful DAGs

For complex, stateful workflows (loops, tool-using agents, retries with memory), consider LangGraph. It lets you define explicit nodes and edges, shared state, and control flow including cycles—useful for agents and long-running processes. Pipelines built with LangGraph are ideal when you need robust orchestration beyond LCEL’s simple branching/parallelism.