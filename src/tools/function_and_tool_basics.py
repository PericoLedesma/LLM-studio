from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from openai import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool


def say_hello(name: str) -> dict:
    return {"tool": "say_hello", "output": {"message": f"Hello, {name}!"}}


# Replace the former arithmetic function with a real tool (DuckDuckGo search)
_search = DuckDuckGoSearchRun()
duckduckgo_search_tool = Tool(
    name="duckduckgo_search",
    func=_search.run,
    description="Search the web for information.",
)


def run_demo() -> None:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Step 1: Ask the model to output RAW JSON function/tool calls (no SDK tools schema)
    system = {
        "role": "system",
        "content": (
            "You are a planner that emits ONLY JSON.\n"
            "- Analyze the user message.\n"
            "- Return a JSON object with key 'calls'.\n"
            "- 'calls' is an array of objects with: name (string), args (object).\n"
            "- Allowed names: say_hello, duckduckgo_search.\n"
            "- Tools:\n"
            "  - say_hello: Greet a person by name.\n"
            "    args schema: {\"name\": \"string\"}\n"
            "  - duckduckgo_search: Search the web for information.\n"
            "    args schema: {\"query\": \"string\"}\n"
            "- Do not include any extra text. No markdown. No explanations.\n\n"
            "Example valid output:\n"
            "{\n  \"calls\": [\n    {\n      \"name\": \"say_hello\",\n      \"args\": {\"name\": \"Pedro\"}\n    },\n    {\n      \"name\": \"duckduckgo_search\",\n      \"args\": {\"query\": \"what are dogs\"}\n    }\n  ]\n}"

            "You dont have to assk the same"
        ),
    }
    user = {"role": "user", "content": "Say hello to Alice and search the web about LLM tools."}

    print("\n*** System instructions: ***")
    print(system["content"])
    print("\n*** User message: ***")
    print(user["content"])
    print("---------")

    # Sending request with instructions
    first_resp_raw = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system, user],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "say_hello",
                    "description": "Greet a person by name.",
                    "parameters": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                        "required": ["name"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "duckduckgo_search",
                    "description": "Search the web for information.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                },
            },
        ],
        tool_choice="auto",
    )
    print("\n*** First RAW response: ***")
    print(first_resp_raw)
    print("----")
    # Response with function calls
    message_content = (first_resp_raw.choices[0].message.content or "").strip()
    print("\n*** Message content (calls=functions that the model wants to call): ***")
    print(message_content)

    # Parsing the response to get the calls
    try:
        parsed = json.loads(message_content)
        calls = parsed.get("calls", []) if isinstance(parsed, dict) else parsed
        print("\n*** Calls: ***")
        print(calls)
    except Exception:
        print("Model returned non-JSON or unexpected format:\n", message_content)
        return

    # Step 2: Execute the calls locally
    outputs = []
    for c in calls:
        name = c.get("name")
        args = c.get("args", {}) or {}
        if name == "say_hello":
            outputs.append(say_hello(name=args.get("name", "")))
        elif name == "duckduckgo_search":
            query = args.get("query", "")
            result = duckduckgo_search_tool.run(query)
            outputs.append({"tool": "duckduckgo_search", "output": result})
        else:
            outputs.append({"tool": name, "error": "unknown tool"})

    # Step 3: Ask the model to compose the final answer using tool outputs
    final_messages = [
        {"role": "system", "content": "Use provided tool outputs to answer succinctly."},
        user,
        {"role": "user", "content": json.dumps({"tool_outputs": outputs})},
    ]

    print("\n*** Final messages: ***")
    print(final_messages)
    print("---------")
    
    print("\n*** Final response: ***")
    final_resp = client.chat.completions.create(model="gpt-4o-mini", messages=final_messages)
    print(final_resp.choices[0].message.content)
    print("---------")


if __name__ == "__main__":
    run_demo()


