from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from openai import OpenAI


def say_hello(name: str) -> dict:
    return {"tool": "say_hello", "output": {"message": f"Hello, {name}!"}}


def add(a: float, b: float) -> dict:
    return {"tool": "add", "output": {"result": a + b}}


def run_demo() -> None:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Step 1: Ask the model to output RAW JSON function calls (no SDK tools)
    system = {
        "role": "system",
        "content": (
            "You are a planner that emits ONLY JSON.\n"
            "- Analyze the user message.\n"
            "- Return a JSON object with key 'calls'.\n"
            "- 'calls' is an array of objects with: name (string), args (object).\n"
            "- Allowed names: say_hello, add.\n"
            "- Do not include any extra text. No markdown. No explanations.\n\n"
            "Example valid output:\n"
            "{\n  \"calls\": [\n    {\n      \"name\": \"say_hello\",\n      \"args\": {\"name\": \"Pedro\"}\n    },\n    {\n      \"name\": \"add\",\n      \"args\": {\"a\": 1, \"b\": 1}\n    }\n  ]\n}"
        ),
    }
    user = {"role": "user", "content": "Say hello to Alice and add 3 and 5."}

    print("\n*** System instructions: ***")
    print(system["content"])
    print("\n*** User message: ***")
    print(user["content"])
    print("---------")

    # Sending request with instructions
    first_resp_raw = client.chat.completions.create(model="gpt-4o-mini", messages=[system, user])
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
        elif name == "add":
            a = float(args.get("a", 0))
            b = float(args.get("b", 0))
            outputs.append(add(a=a, b=b))
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


