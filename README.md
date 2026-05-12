# Roadmap to Master AI Agents

📅 **Learning Journey: Agentic AI + MCP + A2A**

## ⚡ **Quick Setup**

```bash
# Clone and set up
git clone <repo-url>
cd LLM-studio
pip install -r requirements.txt

# Copy and fill in your API keys
cp .env.example .env
```

Required environment variables:
```
OPENAI_API_KEY=sk-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

For local inference: install [Ollama](https://ollama.com) and pull a model (`ollama pull llama3`).

---

## 📊 **Project Overview**

This repository contains a comprehensive learning journey through AI agents, MCP (Model Context Protocol), and multi-agent systems. The project is organized into practical, hands-on examples that build upon each other.

### 🗂️ **Repository Structure**

```
src/
├── agents/                    # Agent building blocks and patterns
│   └── building-blocks/      # Core agent components (intelligence, memory, tools, etc.)
├── langchain_basics/         # LangChain fundamentals and pipelines
├── local_inference/          # Running LLMs locally (llama.cpp, transformers, ollama)
├── mcp/                      # Model Context Protocol implementations
│   ├── basic_example/        # Simple MCP server and client
│   ├── diferent_transports/  # Various transport protocols
│   └── asyncio_lib/          # Async patterns for MCP
├── online_inference/         # Cloud-based LLM inference
│   ├── openai_sdk/           # OpenAI API examples and patterns
│   ├── langchain/            # LangChain online examples
│   └── hugging_face_library/ # Hugging Face integration
├── tools/                    # Function calling and tool integration
├── workflows/                # Advanced workflow patterns and orchestration
└── dockers/                  # Docker containers and FastAPI integration

journal/                      # Learning notes and documentation
├── chains_and_pipelines/     # LangChain concepts
├── mcp/                      # MCP learning materials
├── Running llms/             # Local LLM guides
└── tools/                    # Tool integration guides
```

### 🎯 **Key Accomplishments**

- ✅ **Local LLM Inference**: Complete setup for llama.cpp, Transformers, and Ollama
- ✅ **OpenAI Integration**: Comprehensive examples using official Python SDK
- ✅ **Function Calling**: Advanced tool integration patterns
- ✅ **LangChain Mastery**: Pipelines, agents, and workflow orchestration
- ✅ **MCP Foundation**: Server implementation and multiple transport protocols
- ✅ **Agent Architecture**: Building blocks for intelligent agent systems
- ✅ **Workflow Patterns**: Prompt chaining, routing, and parallelization

---

## 🗺️ **Learning Journey**

The journey is organized as progressive stages — each builds on the previous. Start from Stage 1 if you are new to LLMs, or jump to any stage that matches your current level.

---

### ✅ **Stage 1 – Running LLMs** *(Completed)*

> Goal: Understand what LLMs are, how to run them locally and via cloud APIs.

**Local Inference**
- [x] Run models locally with **llama.cpp** (GGUF format)
  - Server inference (`src/local_inference/llamacpp/server_inference.py`)
  - Python bindings (`src/local_inference/llamacpp/llama.py`)
  - Agent example (`src/local_inference/llamacpp/llama_agent_example.py`)
- [x] Run models locally with **Transformers** (SAFETENSORS format)
  - Download and run HuggingFace models (`src/local_inference/transformers/transformers_basics.py`)
- [x] Run models locally with **Ollama**
  - Server inference (`src/local_inference/ollama/ollama_server.py`)
  - Python subprocess (`src/local_inference/ollama/ollama_subprocess.py`)
  - Chat interface (`src/local_inference/ollama/ollama_chat.py`)
  - LangChain integration (`src/local_inference/ollama/ollama_with_langchain.py`)

**Online Inference**
- [x] **OpenAI API** basics (`src/online_inference/openai_sdk/01-introduction.py`)
  - Streaming responses (`src/online_inference/openai_sdk/02-streaming.py`)
  - Structured output / JSON mode (`src/online_inference/openai_sdk/structured_output/`)
  - Reasoning models (`src/online_inference/openai_sdk/responses/08-reasoning.py`)
- [x] **Hugging Face** API (`src/online_inference/hugging_face_library/`)

---

### ✅ **Stage 2 – LangChain & Integration Patterns** *(Completed)*

> Goal: Learn how to chain LLM calls, use LangChain abstractions, and build pipelines.

- [x] LangChain core components (`src/langchain_basics/langchain_components.py`)
- [x] Pipelines and chains (`src/langchain_basics/pipelines.py`)
- [x] LangGraph basics (`src/langchain_basics/graph.py`)
- [x] LangChain online examples (`src/online_inference/langchain/langchain_example.py`)

---

### ✅ **Stage 3 – Tools & Function Calling** *(Completed)*

> Goal: Give LLMs the ability to take actions by calling tools and functions.

- [x] Raw function basics (`src/tools/raw_functions_basics.py`)
- [x] Function and tool fundamentals (`src/tools/function_and_tool_basics.py`)
- [x] Creating custom tools (`src/tools/creating_tools.py`)
- [x] Experimenting with functions (`src/tools/experimenting_functions.py`)
- [x] OpenAI SDK function calling (`src/online_inference/openai_sdk/responses/04-function-calling.py`)
- [x] OpenAI SDK structured output for tool calls (`src/online_inference/openai_sdk/structured_output/03-function-calling.py`)

---

### ✅ **Stage 4 – Workflow Patterns** *(Completed)*

> Goal: Compose LLM calls into robust, multi-step workflows.

- [x] Workflow introduction (`src/workflows/1-introduction/`)
  - Basic, structured, with tools, with retrieval (RAG)
- [x] Prompt chaining (`src/workflows/2-workflow-patterns/1-prompt-chaining.py`)
- [x] Routing (`src/workflows/2-workflow-patterns/2-routing.py`)
- [x] Parallelization (`src/workflows/2-workflow-patterns/3-parallizaton.py`)
- [x] Orchestrator pattern (`src/workflows/2-workflow-patterns/4-orchestrator.py`)
- [ ] Design patterns deep-dive (`src/workflows/3-design-patterns/`) *(planned)*

---

### ✅ **Stage 5 – Agent Architecture** *(Completed)*

> Goal: Build agents that reason, remember, and act autonomously.

- [x] Intelligence — reasoning and decision-making (`src/agents/building-blocks/1-intelligence.py`)
- [x] Memory — short and long-term context (`src/agents/building-blocks/2-memory.py`)
- [x] Tools — equipping agents with capabilities (`src/agents/building-blocks/3-tools.py`)
- [x] Validation — output verification (`src/agents/building-blocks/4-validation.py`)
- [x] Control flow — loops and conditions (`src/agents/building-blocks/5-control.py`)
- [x] Recovery — error handling and retries (`src/agents/building-blocks/6-recovery.py`)
- [x] Feedback — evaluation and self-improvement (`src/agents/building-blocks/7-feedback.py`)
- [x] Simple agent with LangChain (`src/langchain_basics/simple_agent.py`)
- [x] OpenAI SDK multi-agent basics (`src/online_inference/openai_sdk/agents/01-introduction.py`)
- [x] OpenAI SDK agent handoffs (`src/online_inference/openai_sdk/agents/02-handoffs.py`)

---

### ✅ **Stage 6 – MCP (Model Context Protocol)** *(Completed)*

> Goal: Expose tools and resources to AI agents using the standardized MCP protocol.

- [x] What is MCP and why it matters (`journal/mcp/whatisMCP.md`)
- [x] Basic MCP server (`src/mcp/basic_example/mcp_server.py`)
- [x] Basic MCP client — calling the server (`src/mcp/basic_example/call_your_server.py`)
- [x] Listing and using tools via MCP (`src/mcp/basic_example/list_tools.ipynb`, `use_tools.ipynb`)
- [x] Transport protocols
  - SSE (`src/mcp/diferent_transports/client-sse.py`)
  - stdio (`src/mcp/diferent_transports/client-stdio.py`)
  - Streamable HTTP (`src/mcp/diferent_transports/client-streamable-http.py`)
- [x] Async MCP patterns (`src/mcp/asyncio_lib/asyncio_lib.py`)
- [x] Docker containerization for MCP (`src/mcp/run-with-docker/`)
- [x] Lifecycle management (`src/mcp/lifecycle-management/`)

---

### 🔄 **Stage 7 – Multi-Agent Systems (A2A)** *(In Progress)*

> Goal: Build systems where multiple agents collaborate, delegate, and communicate.

- [ ] Multi-agent coordination — agents working on shared tasks
- [ ] Agent-to-Agent (A2A) communication — message passing between agents
- [ ] Advanced workflow orchestration — chaining agents across complex tasks
- [ ] Error handling and recovery in multi-agent pipelines
- [ ] Performance optimization — parallelism and load balancing
- [ ] Deployment strategies — running agent systems in production

---

### 📋 **Stage 8 – Capstone Project** *(Planned)*

> Goal: End-to-end agentic system combining all skills — MCP, A2A, orchestration, deployment.

- [ ] Define problem domain and agent roles
- [ ] Build the orchestrator and specialist agents
- [ ] Integrate MCP for tool exposure
- [ ] Implement A2A communication
- [ ] Add observability with Langfuse
- [ ] Deploy and test end-to-end

---

## 📊 **Langfuse Integration & Tracing** *(Planned)*

> **Status:** Not yet implemented. The integrations below are planned for `src/online_inference/langfuse/`.

Langfuse will be used for tracing, monitoring, and analyzing LLM and agent workflows across all stages. Planned coverage:

- **General setup** — SDK initialization, environment configuration
- **Pipelines** — trace LangChain pipelines end-to-end
- **Function calling** — capture tool inputs, outputs, and latency
- **Response logging** — log and analyze raw LLM responses
- **Agent tracing** — trace agent reasoning steps and tool usage
- **Workflow tracing** — trace multi-step orchestrations
- **MCP requests** — trace server/client interactions
- **Multi-agent** — trace A2A message passing and delegation

---

### 📚 **Learning Path**

Follow stages in order if starting from scratch:

1. **Stage 1** — Run your first LLM locally with Ollama, then try the OpenAI API (`src/online_inference/openai_sdk/`)
2. **Stage 2** — Chain LLM calls with LangChain (`src/langchain_basics/`)
3. **Stage 3** — Give the LLM tools to call (`src/tools/`)
4. **Stage 4** — Build multi-step workflows (`src/workflows/`)
5. **Stage 5** — Assemble a full agent with memory and control flow (`src/agents/building-blocks/`)
6. **Stage 6** — Expose capabilities via MCP (`src/mcp/`)
7. **Stage 7** — Connect multiple agents together *(coming next)*

---

## 📓 **Supporting Notes (journal/)**

Each stage has accompanying theory notes in `journal/`. Read these alongside the code for deeper understanding.

| Topic | Notes |
|-------|-------|
| Running LLMs | `journal/Running llms/` — model formats (GGUF, SAFETENSORS), llama ecosystem, Ollama, online inference, LangChain ecosystem |
| Tools | `journal/tools/` — function calling basics, tool design, using tools with agents |
| Chains & Pipelines | `journal/chains_and_pipelines/` — differences between chains, pipelines, and agents |
| MCP | `journal/mcp/` — what MCP is, server/client concepts, asyncio, Docker for dummies |
| Docker | `journal/mcp/dockers_for_dummies.md` + `journal/Running llms/` — containerization basics |

---

## 📝 **Development Guidelines**

### Git Commit Conventions
- `feat:` → new feature
- `fix:` → bug fix  
- `refactor:` → code restructuring
- `docs:` → documentation changes
- `test:` → adding/updating tests
- `chore:` → minor updates or tooling

### Code Standards
- Use type hints for all functions
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Write modular, testable code
- Use the official OpenAI Python SDK (not requests library)
