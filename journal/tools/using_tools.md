# Using tools with LLMs: three practical patterns

This guide shows three reliable ways to let an LLM call your functions/tools, when to use each, and minimal runnable examples. Examples use the official OpenAI Python SDK, aligning with function/tool calling features.

- **Approach 1 — OpenAI SDK native tool calling (functions)**: The model decides if/when to call tools you expose.
- **Approach 2 — Manual planner + router**: You control planning/validation and route to tools deterministically.
- **Approach 3 — LangChain agent with tools**: A batteries‑included agent selects and invokes tools for you.

---

### 1) OpenAI SDK native tool calling (functions)

Best when you want the model to autonomously decide whether to call a function and with what arguments. You define tool schemas (name, description, JSON params). The model returns `tool_calls`; you execute them and send results back for the final answer.

Key points:
- Define tools with clear names, descriptions, and JSON Schema parameters.
- Handle multiple tool calls in sequence if the model requests them.
- Always validate/guard inputs before executing side effects.

Minimal example:

```python
from typing import Dict, Any
from openai import OpenAI

client = OpenAI()

def get_weather(city: str, unit: str = "c") -> Dict[str, Any]:
    # Dummy implementation; replace with a real API call.
    temp_c = 22.5
    if unit.lower() == "f":
        temp = temp_c * 9 / 5 + 32
        unit_label = "F"
    else:
        temp = temp_c
        unit_label = "C"
    return {"city": city, "temperature": temp, "unit": unit_label}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current temperature for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["c", "f"], "description": "Temperature unit"}
                },
                "required": ["city"]
            },
        },
    }
]

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the temperature in Madrid in F?"},
]

# Step 1: let the model decide to call a tool
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

msg = resp.choices[0].message
tool_calls = msg.tool_calls or []

if tool_calls:
    # Execute each tool call and append results as tool messages
    for call in tool_calls:
        if call.function.name == "get_weather":
            args = call.function.arguments  # JSON string in some SDK versions; dict in others
            if isinstance(args, str):
                import json
                args = json.loads(args)
            result = get_weather(city=args["city"], unit=args.get("unit", "c"))
            messages.append({"role": "tool", "tool_call_id": call.id, "name": "get_weather", "content": str(result)})

    # Step 2: ask the model to produce the final answer with tool results
    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages + [{"role": "assistant", "content": None, "tool_calls": tool_calls}],
    )
    print(final.choices[0].message.content)
else:
    # No tool call needed; just answer
    print(msg.content)
```

When to use:
- You trust the model to choose tools well, and you want minimal orchestration.
- You need multi-tool reasoning with minimal custom routing code.

---

### 2) Manual planner + router pattern

Best when you want deterministic control, validations, or guardrails. The model emits a tiny JSON "plan" describing which tool to call and with what arguments; your code validates and executes it, then asks the model to verbalize a user-friendly answer.

Prompting strategy:
- Constrain the model to output a strict JSON object with `tool` and `args`.
- Validate JSON and arguments; reject/repair if needed.
- Execute, then optionally ask the model to explain results for the end user.

Minimal example:

```python
import json
from typing import Dict, Any
from openai import OpenAI

client = OpenAI()

def get_weather(city: str, unit: str = "c") -> Dict[str, Any]:
    temp_c = 22.5
    if unit.lower() == "f":
        temp = temp_c * 9 / 5 + 32
        unit_label = "F"
    else:
        temp = temp_c
        unit_label = "C"
    return {"city": city, "temperature": temp, "unit": unit_label}

SYSTEM = """
You are a planner. Output ONLY a compact JSON with keys: tool, args.
Tools: get_weather(city: string, unit: 'c'|'f').
If no tool applies, use tool: "none" and args: {}.
"""

USER = "What's the temperature in Madrid in F?"

plan_resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER},
    ],
)

raw = plan_resp.choices[0].message.content or "{}"
try:
    plan = json.loads(raw)
except json.JSONDecodeError:
    raise ValueError(f"Planner returned non-JSON: {raw}")

tool = plan.get("tool")
args = plan.get("args", {})

if tool == "get_weather":
    city = args.get("city")
    unit = args.get("unit", "c")
    if not isinstance(city, str):
        raise ValueError("city is required and must be a string")
    if unit not in ("c", "f"):
        raise ValueError("unit must be 'c' or 'f'")
    result = get_weather(city, unit)
elif tool == "none":
    result = {"note": "No tool necessary"}
else:
    raise ValueError(f"Unknown tool: {tool}")

# Verbalize final answer
final_resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You explain results clearly and concisely."},
        {"role": "user", "content": USER},
        {"role": "assistant", "content": f"Tool result: {json.dumps(result)}"},
    ],
)

print(final_resp.choices[0].message.content)
```

When to use:
- You need strict validation, audit trails, or pre-approval before executing side effects.
- You want clear separation of planning and execution.

---

### 3) LangChain agent with tools

Best for rapid prototyping with built-in agent loops and observation handling. You decorate Python functions as tools; the agent handles selection and calling. This adds dependencies and abstraction but can speed up development.

Minimal example (LCEL/AgentExecutor):

```python
from typing import Annotated
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate

@tool
def get_weather(city: str, unit: str = "c") -> str:
    """Get the current temperature for a city. unit is 'c' or 'f'."""
    temp_c = 22.5
    if unit.lower() == "f":
        temp = temp_c * 9 / 5 + 32
        unit_label = "F"
    else:
        temp = temp_c
        unit_label = "C"
    return f"{city}: {temp} {unit_label}"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_weather]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

result = executor.invoke({"input": "What's the temperature in Madrid in F?"})
print(result["output"])
```

When to use:
- You prefer a higher-level framework with built-in patterns, logging, and memory integrations.
- Quick demos or POCs where agent orchestration is convenient.

---

### Choosing the right approach

- **Use OpenAI native tools** when you want simple, robust function calling with minimal glue code.
- **Use Manual planner + router** when you need validations, approvals, or deterministic control over side effects.
- **Use LangChain agent** for rapid prototyping and when leveraging the LangChain ecosystem is valuable.

### Implementation tips and pitfalls

- **Validate inputs**: Even with tool schemas, validate before hitting external systems.
- **Idempotency**: For side-effectful tools (e.g., payments, emails), include correlation IDs.
- **Observability**: Log tool requests/responses, timestamps, and user/session IDs.
- **Tool design**: Prefer small, purpose-driven tools with clear JSON schemas and enums.
- **Security**: Avoid exposing raw filesystem/network ops; wrap them with policy checks.
- **Model choice**: Use function-capable models. Smaller models may hallucinate arguments more.
- **User experience**: Return helpful, concise final answers; avoid dumping raw tool JSON to end users.

---

### Related files in this repo

- `src/agents/creating_tools.py`: High-level overview of the three patterns.
- `src/agents/function_and_tool_basics.py`: Basics of defining functions/tools for model use.
- `src/agents/raw_functions_basics.py`: Lower-level examples of calling functions.
- `src/agents/tools.py`: Simple tool definitions used by agents.
- `src/langchain_basics/simple_agent.py`: Example of a simple LangChain agent.

Copy snippets as needed and adapt to your APIs and models.


