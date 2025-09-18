"""
Three different ways to use tools with an LLM:

1) OpenAI SDK native tool calling (functions)
   - Best when you want the model to decide if/when to call your functions.
   - You define tool schemas (name, description, JSON params), the model returns tool_calls,
     you execute them, then give results back for the final answer.

2) Manual planner + router pattern
   - Best when you want full control over planning, routing, and guardrails.
   - The model emits a tiny JSON plan describing which tool to use and with what args.
     You validate, route, execute, and optionally ask the model to verbalize the result.

3) LangChain agent with tools
   - Best for quick prototyping with batteries-included orchestration.
   - You decorate Python functions as tools; the agent handles selection and calling.
"""

import json
from typing import Any, Dict, Optional


# ========== 1) OpenAI SDK native tool calling ==========
# Uses the official OpenAI Python SDK (no requests), per your preference.
# Flow:
#   Step 1: Define tool schemas (JSON parameters, required fields).
#   Step 2: First model call: the LLM may emit tool_calls with arguments.
#   Step 3: Execute the called tools in Python and append a tool message with the result.
#   Step 4: Second model call: the LLM produces a final, human-friendly response.

def example_openai_tool_calling() -> None:
    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai")
        return

    client = OpenAI()

    # Tool schema (what the model sees and reasons over)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"},
                        "unit": {"type": "string", "enum": ["c", "f"], "default": "c"},
                    },
                    "required": ["city"],
                },
            },
        }
    ]

    def get_weather(city: str, unit: str = "c") -> Dict[str, Any]:
        # Minimal input sanity checks (defense-in-depth)
        if not isinstance(city, str) or not city.strip():
            return {"error": {"code": "BAD_INPUT", "message": "city must be a non-empty string"}}
        if unit not in ("c", "f"):
            unit = "c"
        # Stub: replace with a real API call (handle timeouts/retries)
        return {"city": city, "temperature": 22, "unit": unit, "condition": "sunny"}

    messages = [
        {"role": "user", "content": "What's the weather in Madrid in celsius?"}
    ]

    # Step 1: model may decide to call a tool
    first = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0,
    )

    tool_calls = first.choices[0].message.tool_calls or []
    if not tool_calls:
        # Model answered directly without tools
        print(first.choices[0].message.content)
        return

    # Step 2: execute tool(s) and append results
    for call in tool_calls:
        name = call.function.name
        try:
            args = json.loads(call.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}

        if name == "get_weather":
            result = get_weather(**args)
        else:
            result = {"error": {"code": "UNKNOWN_TOOL", "message": f"{name}"}}

        messages.append(
            {
                "role": "tool",
                "tool_call_id": call.id,
                "name": name,
                "content": json.dumps(result),
            }
        )

    # Step 3: final answer using tool outputs
    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
    )
    print(final.choices[0].message.content)

    # Production notes:
    # - Add timeouts/retries for tool executions and SDK calls.
    # - Log tool name, args, latency, and result size for observability.
    # - Consider Pydantic or JSON Schema validation on the Python side too.


# ========== 2) Manual planner + router ==========
# The model emits a JSON plan; you validate and route. This gives you:
# - Strong control over tool selection and arguments
# - Easier guardrails and auditing
# - Optional second LLM pass to verbalize the result

def example_manual_planner_router() -> None:
    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai")
        return

    client = OpenAI()

    # Your internal toolbox (pure Python)
    def sum_two(a: Any, b: Any) -> int:
        try:
            return int(a) + int(b)
        except Exception:
            raise ValueError("sum_two requires integer-like a and b")

    def repeat(text: Any, n: Any = 1) -> str:
        n = int(n)
        return (" ".join([str(text)] * n)).strip()

    TOOLBOX = {"sum_two": sum_two, "repeat": repeat}

    def validate_plan(obj: Dict[str, Any]) -> Optional[str]:
        # Minimal validator for the planner JSON
        if "final" in obj:
            if not isinstance(obj["final"], str):
                return "final must be a string"
            return None

        tool = obj.get("tool")
        args = obj.get("args", {})
        if tool not in TOOLBOX:
            return f"unknown tool: {tool}"
        if not isinstance(args, dict):
            return "args must be an object"
        # Add per-tool arg checks if needed
        return None

    system = (
        "You are a planner. Decide one tool to use from {tools}.\n"
        'Return ONLY JSON: {\"tool\": \"<name>\", \"args\": {...}}\n'
        'If no tool is needed, return {\"final\": \"<answer>\"}.'
    ).format(tools=list(TOOLBOX.keys()))

    user = "Add 41 and 1, then stop."

    plan_text = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0,
    ).choices[0].message.content

    try:
        plan_obj = json.loads(plan_text or "{}")
    except json.JSONDecodeError:
        print("Planner returned non-JSON. Raw:", plan_text)
        return

    err = validate_plan(plan_obj)
    if err:
        print(f"Invalid plan: {err}")
        return

    if "final" in plan_obj:
        print(plan_obj["final"])
        return

    tool_name = plan_obj["tool"]
    args = plan_obj.get("args", {})

    try:
        result = TOOLBOX[tool_name](**args)
    except Exception as e:
        result = {"error": {"code": "TOOL_EXECUTION_ERROR", "message": str(e)}}

    # Optional second pass to verbalize neatly
    verbalized = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Explain the tool result briefly."},
            {"role": "user", "content": f"Tool {tool_name} returned: {json.dumps(result)}"},
        ],
        temperature=0,
    ).choices[0].message.content

    print(verbalized)

    # Production notes:
    # - Persist the plan and execution for auditability.
    # - Add per-tool input schemas and strict validation.
    # - Rate-limit tools and enforce timeouts.


# ========== 3) LangChain agent with tools ==========
# Quick demonstration using LangChain's tool-calling agent.
# Notes:
# - @tool-decorated functions become callable tools.
# - The agent determines which tools to call and in what order.
# - Configure your OpenAI key as environment variable for ChatOpenAI.

def example_langchain_agent() -> None:
    try:
        from langchain.tools import tool
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError:
        print("pip install langchain langchain-openai")
        return

    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two integers. Args: a (int), b (int). Returns product (int)."""
        return int(a) * int(b)

    @tool
    def upper(text: str) -> str:
        """Uppercase a string. Args: text (str)."""
        return text.upper()

    tools = [multiply, upper]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Use tools when helpful."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    result = executor.invoke({"input": "What is 7 * 6? Then uppercase 'done'."})
    print(result["output"])

    # Production notes:
    # - Use tool descriptions to constrain when/why tools are used.
    # - Set max_iterations / handle timeouts on agent executors.
    # - Add callbacks for logging tool usage and costs.


if __name__ == "__main__":
    print("=== 1) OpenAI SDK native tool calling ===")
    example_openai_tool_calling()
    print("--------------------------------\n")

    print("\n=== 2) Manual planner + router ===")
    example_manual_planner_router()
    print("--------------------------------\n")

    print("\n=== 3) LangChain agent with tools ===")
    example_langchain_agent()
    print("--------------------------------\n")
