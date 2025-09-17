# 🧠 LangChain Architecture Overview

LangChain is a modular framework for building applications powered by large language models (LLMs). It provides a rich ecosystem of libraries and components that work together to support chains, agents, memory, and more.

---

## 📦 Core Components & Supporting Libraries

| **Component**                          | **Description**                                                     | **Library**                        |
|----------------------------------------|---------------------------------------------------------------------|------------------------------------|
| `LangChain Core`                       | Foundational abstractions for LLMs, chains, tools, memory, and LCEL | `langchain-core`                   |
| `LangChain Expression Language (LCEL)` | Declarative syntax for composing chains and agents                  | `langchain-core`                   |
| `Chains`                               | Sequences of calls that form workflows                              | `langchain`, `langchain-core`      |
| `Agents`                               | Autonomous entities that use tools to accomplish tasks              | `langchain`, `langchain-core`      |
| `Tools`                                | External functions or APIs (e.g., search, calculator)               | `langchain`, `langchain-community` |
| `Memory`                               | Stores and retrieves context across interactions                    | `langchain`, `langchain-core`      |
| `Callbacks`                            | Hooks for logging, tracing, and monitoring execution                | `langsmith`, `langchain-core`      |
| `LangGraph`                            | Graph-based orchestration for stateful, multi-step workflows        | `langgraph`                        |



## 🔧 Library Summary

| **Library**           | **Purpose**                                                                   |
|-----------------------|-------------------------------------------------------------------------------|
| `langchain-core`      | Base abstractions and LCEL for composing workflows                            |
| `langchain`           | High-level components for chains, agents, and memory                          |
| `langchain-community` | Integrations with third-party services (OpenAI, Pinecone, Hugging Face, etc.) |
| `langchain-openai`    | Lightweight wrapper for OpenAI models                                         |
| `langchain-anthropic` | Wrapper for Anthropic models                                                  |
| `langgraph`           | Graph-based orchestration for complex workflows                               |
| `langsmith`           | Monitoring, debugging, and evaluation tools                                   |


## 🧬 Internal Schema of LangChain

LangChain:
  LLMs:
    - Providers: [OpenAI, Anthropic, Cohere, HuggingFace]
    - Interface: ChatModel, CompletionModel

  Prompts:
    - Templates: PromptTemplate, ChatPromptTemplate
    - Formatters: FewShotPrompt, StructuredPrompt

  Chains:
    - Types: LLMChain, SequentialChain, RouterChain
    - Composition: LCEL (LangChain Expression Language)

  Agents:
    - Types: ReActAgent, ToolAgent, PlanAndExecuteAgent
    - Components:
        - AgentExecutor
        - AgentToolkits
        - AgentPlanner

  Tools:
    - Built-in: Search, Calculator, Python REPL
    - Custom: API wrappers, user-defined functions

  Memory:
    - Types: BufferMemory, SummaryMemory, EntityMemory
    - Usage: Stores conversation history and context

  Callbacks:
    - Tracing: LangSmith
    - Logging: Console, File, Remote

  Output Parsers:
    - Types: StructuredOutputParser, RegexParser
    - Purpose: Validate and format LLM responses

---

### 🔌 Integrations

| Category             | Examples                                             |
|----------------------|------------------------------------------------------|
| **LLM Providers**    | OpenAI, Anthropic, Cohere, Hugging Face, Google PaLM |
| **Embedding Models** | OpenAI, Cohere, Hugging Face, TensorFlow             |
| **Vector Stores**    | Pinecone, Weaviate, FAISS, Chroma, Milvus            |
| **Databases**        | MongoDB, PostgreSQL, Redis, Supabase                 |
| **Document Loaders** | PDF, HTML, CSV, Notion, Slack, Google Docs           |
| **Toolkits**         | SerpAPI, Wolfram Alpha, Zapier, Browser, Calculator  |

### 🛠️ Development Tools

- **LangSmith**: Observability and debugging platform for LangChain applications.  
- **LangServe**: Tool for deploying LangChain chains as REST APIs.  
- **LangChainHub**: Repository of community-contributed chains and agents.  

### 🚀 Deployment Options

- **Local**: Python, JavaScript  
- **Serverless**: e.g., Vercel, AWS Lambda  
- **Containerized**: Docker  
- **API-based**: LangServe, FastAPI
- 
---------- 











