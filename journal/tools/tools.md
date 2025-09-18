# Tools in LLM Agents

Tools are external capabilities an LLM can invoke to extend its abilities beyond plain text generation. Common examples include web search, databases, code execution, file I/O, math/solver APIs, and custom business functions.

### Core Ideas
- **Schema-first**: Each tool is defined by a name, description, and parameters schema. The model chooses when and how to call it.
- **Single-turn or multi-turn**: The agent can call one or multiple tools, receive results, then continue reasoning.
- **Deterministic interfaces**: Tools should be idempotent, validated, and return structured outputs.

### Minimal Anatomy of a Tool
```json
{
  "name": "search_docs",
  "description": "Search internal documents by keyword",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Search query"},
      "limit": {"type": "integer", "minimum": 1, "maximum": 20}
    },
    "required": ["query"]
  }
}
```

### Execution Flow (High-level)
1. Model plans and decides a tool call with arguments.
2. Runtime validates args against the tool schema.
3. Host executes the tool and returns structured result.
4. Model consumes the result and continues or finalizes the answer.

### Design Guidelines
- **Keep tools small and composable**: One responsibility per tool.
- **Write clear descriptions**: Explain when to use the tool and what it returns.
- **Validate inputs**: Enforce types, ranges, and required fields.
- **Return structured data**: Prefer JSON-like objects over raw strings.
- **Avoid side-effects by default**: Unless intentional and documented.
- **Log usage**: Capture name, args, latency, success/error for observability.

### Good Tool Descriptions
- Be explicit about: purpose, inputs, outputs, constraints, and edge cases.
- Include units (e.g., ms, USD) and domains (e.g., UTC for times).

### Error Handling
- Return machine-readable errors: `{ "error": { "code": "NOT_FOUND", "message": "..." } }`.
- Keep failures non-fatal to the conversation; allow the model to recover.

### Security & Safety
- Whitelist accessible resources; never trust model-produced paths/URLs blindly.
- Sanitize inputs; rate-limit and time-limit execution.
- Redact sensitive data from logs and tool outputs when possible.

### When Not to Create a Tool
- If the task is purely linguistic or can be answered from the prompt/context window.
- If adding a tool increases complexity without improving accuracy or latency.

### Example Result Contract
```json
{
  "results": [
    {"id": "doc_123", "title": "Intro", "score": 0.82},
    {"id": "doc_456", "title": "Setup", "score": 0.77}
  ],
  "took_ms": 34
}
```

Keep tool interfaces boring, typed, and predictable—the model performs best with simple, well-documented contracts.


