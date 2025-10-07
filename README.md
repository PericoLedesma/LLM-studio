# Roadmap to Master AI Agents

📅 **Learning Journey: 3 Months (Agentic AI + MCP + A2A)**

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
└── workflows/                # Advanced workflow patterns and orchestration

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

## 🎯 **Current Status: Month 1 - Foundations (In Progress)**

### ✅ **Week 1 – Running LLMs (COMPLETED)**
- [x] **Day 1:** Running models locally intro
- [x] **Day 2:** Online inference intro  
- [x] **Day 3:** Download and run models locally
  - **llama.cpp (GGUF format)** ✅
    - Server inference (`src/local_inference/llamacpp/server_inference.py`)
    - Python bindings (`src/local_inference/llamacpp/llama.py`)
  - **Transformers (SAFETENSORS format)** ✅
    - Multiple download options (`src/local_inference/transformers/transformers_basics.py`)
  - **Ollama** ✅
    - Server inference (`src/local_inference/ollama/ollama_server.py`)
    - Python bindings (`src/local_inference/ollama/ollama_subprocess.py`)
- [x] **Day 4:** Online inference with OpenAI + LangChain
  - **OpenAI API (Python SDK)** ✅ (`src/online_inference/openai_sdk/`)
  - **LangChain basics** ✅ (`src/langchain_basics/`)
- [x] **Day 5:** Functions & Pipelines ✅
  - Function calling examples (`src/online_inference/openai_sdk/responses/04-function-calling.py`)
  - LangChain pipelines (`src/langchain_basics/pipelines.py`)

### ✅ **Week 2 – Agent Basics (COMPLETED)**
- [x] **Day 6:** Simple agent loop implementation ✅
  - Basic agent building blocks (`src/agents/building-blocks/`)
  - Intelligence, memory, tools, validation, control, recovery, feedback
- [x] **Day 7:** Function calling with LLMs ✅
  - Comprehensive tool examples (`src/tools/`)
  - OpenAI SDK function calling (`src/online_inference/openai_sdk/responses/04-function-calling.py`)
- [x] **Day 8:** Structured output and responses ✅
  - JSON mode examples (`src/online_inference/openai_sdk/structured_output/`)
  - Response handling patterns (`src/online_inference/openai_sdk/responses/`)
- [x] **Day 9:** LangChain agents and tools ✅
  - Simple agent implementation (`src/langchain_basics/simple_agent.py`)
  - Tool creation and experimentation (`src/tools/`)
- [x] **Day 10:** Workflow patterns ✅
  - Basic workflows (`src/workflows/1-introduction/`)
  - Prompt chaining (`src/workflows/2-workflow-patterns/1-prompt-chaining.py`)

### 🔄 **Week 3 – MCP Foundation (IN PROGRESS)**
- [x] **Day 11:** MCP server basics ✅
  - Basic MCP server (`src/mcp/basic_example/mcp_server.py`)
  - Client implementation (`src/mcp/basic_example/call_your_server.py`)
- [x] **Day 12:** MCP transports ✅
  - Multiple transport examples (`src/mcp/diferent_transports/`)
  - SSE, stdio, and HTTP transports
- [x] **Day 13:** Async MCP patterns ✅
  - AsyncIO library examples (`src/mcp/asyncio_lib/`)
- [x] **Day 14:** Docker containerization
- [ ] **Day 15:** Small project: linkedin post swarm of agents

### 📋 **Week 4 – Advanced Patterns (PLANNED)**

- [ ] **Day 16:** Multi-agent coordination  
  - Introduction to coordinating multiple agents  
  - Simple examples of agents working together on a shared task

- [ ] **Day 17:** Agent-to-Agent communication  
  - Basics of sending messages between agents  
  - Practice with simple message passing

- [ ] **Day 18:** Workflow orchestration  
  - Overview of chaining tasks and agents  
  - Build a basic multi-step workflow

- [ ] **Day 19:** Error handling and recovery  
  - Learn how to catch and handle errors in agent workflows  
  - Add simple retry logic

- [ ] **Day 20:** Performance optimization  
  - Identify slow parts of your workflow  
  - Try out basic improvements (e.g., running steps in parallel)

- [ ] **Day 21:** Deployment strategies  
  - Discuss simple ways to run your agent system outside your development environment  
  - Try running your workflow on a different machine or server

#### 📚 **Additional Learning Areas**
- [ ] Model training on local hardware
- [ ] PyTorch checkpoint analysis
- [ ] Advanced transformer architectures

---

## 📊 **Langfuse Integration & Tracing**

Langfuse is used throughout this project for tracing, monitoring, and analyzing LLM and agent workflows. Key integration points include:

- **General Integration:**  
  - Langfuse setup and basic usage (`src/online_inference/langfuse/`)
- **Pipelines:**  
  - Tracing for pipelines (`src/online_inference/langfuse/pipeline_tracing.py`)
- **Function Calling:**  
  - Tracing function calls (`src/online_inference/langfuse/function_call_tracing.py`)
- **Response Logging:**  
  - Logging and analyzing LLM responses (`src/online_inference/langfuse/response_logging.py`)
- **Agent Tracing:**  
  - Tracing agent execution and tool usage (`src/online_inference/langfuse/agent_tracing.py`)
- **Workflow Tracing:**  
  - Tracing multi-step workflows (`src/online_inference/langfuse/workflow_tracing.py`)
- **MCP Requests:**  
  - Tracing MCP server/client interactions (`src/online_inference/langfuse/mcp_tracing.py`)
- **Multi-agent and Communication:**  
  - Planned: Tracing for multi-agent workflows and message passing
- **Advanced Analytics:**  
  - Planned: Custom analytics and advanced tracing (`src/online_inference/langfuse/`)

Langfuse helps visualize, debug, and optimize all stages of LLM and agent development in this repository.

---

## 🚀 **Month 2 – 

### **Week 5 – 


### **Week 6 –

### **Week 7 – 

### **Week 8 –

---

## 🏆 **Month 3 – Capstone Project:

### **Week 9-12 – End-to-End Implementation**


---

### 📚 **Learning Path**
1. Start with `src/online_inference/openai_sdk/` for OpenAI basics
2. Explore `src/local_inference/` for local LLM setup
3. Dive into `src/tools/` for function calling
4. Study `src/workflows/` for advanced patterns
5. Build agents with `src/agents/building-blocks/`

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