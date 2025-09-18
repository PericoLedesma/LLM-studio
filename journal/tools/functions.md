# Calls vs. Functions with an LLM

- **Calls (plan)**: A structured instruction from the LLM describing which function to run and with what arguments. It’s a declarative plan, not executable code.
- **Functions (implementation)**: Your actual Python functions that do the work. Your code maps each call to the right function and executes it.

### Why this split
- **Reliability**: The LLM outputs a machine-readable plan (JSON).
- **Control**: You validate/execute only allowed functions with typed args.
- **Security**: Reduces prompt injection via free-form prose.

### Example

LLM output (plan):
```json
{
  "calls": [
    {"name": "say_hello", "args": {"name": "Alice"}},
    {"name": "add", "args": {"a": 3, "b": 5}}
  ]
}
```

Your functions (implementation):
```python
def say_hello(name: str) -> dict:
    return {"tool": "say_hello", "output": {"message": f"Hello, {name}!"}}

def add(a: float, b: float) -> dict:
    return {"tool": "add", "output": {"result": a + b}}
```

Dispatcher (how it works together):
```python
for call in calls:
    name, args = call["name"], call.get("args", {})
    if name == "say_hello":
        out = say_hello(**args)
    elif name == "add":
        out = add(**args)
    else:
        out = {"tool": name, "error": "unknown tool"}
    tool_outputs.append(out)
```

Compose final answer:
- Send the original user message + `tool_outputs` to the LLM.
- The LLM crafts a natural-language response based on the tool results.

### Flow summary
1. User asks something.
2. LLM returns JSON `calls` (the plan).
3. Your code executes mapped Python functions.
4. You pass `tool_outputs` back to the LLM.
5. LLM returns the final user-facing answer.