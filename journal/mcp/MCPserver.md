# MCP Servers

MCP servers are programs that expose specific capabilities to AI applications through standardized protocol interfaces.

## Core Server Features

MCP servers provide functionality through three building blocks:

| Feature | Description | Examples | Control |
|---------|-------------|----------|---------|
| **Tools** | Functions that LLMs can actively call and decide when to use based on user requests | • Search flights<br>• Send messages<br>• Create calendar events | Model decides |
| **Resources** | Passive data sources providing read-only access to information for context | • Retrieve documents<br>• Access knowledge bases<br>• Read calendars | Application provides |
| **Prompts** | Pre-built instruction templates that guide the model to work with specific tools and resources | • Plan a vacation<br>• Summarize meetings<br>• Draft an email | Pre-configured |

## Tools Deep Dive

Tools enable AI models to perform actions. Each tool defines a specific operation with typed inputs and outputs.

### How Tools Work

- **Schema-defined interfaces** that LLMs can invoke
- **JSON Schema validation** for input/output
- **Single operation focus** with clearly defined parameters
- **User consent** may be required before execution

### Protocol Operations

| Method | Purpose | Returns |
|--------|---------|---------|
| `tools/list` | Discover available tools | Array of tool definitions with schemas |
| `tools/call` | Execute a specific tool | Tool execution result |

### Example Tool Definition

```json
{
  "name": "searchFlights",
  "description": "Search for available flights",
  "inputSchema": {
    "type": "object",
    "properties": {
      "origin": { 
        "type": "string", 
        "description": "Departure city" 
      },
      "destination": { 
        "type": "string", 
        "description": "Arrival city" 
      },
      "date": { 
        "type": "string", 
        "format": "date", 
        "description": "Travel date" 
      }
    },
    "required": ["origin", "destination", "date"]
  }
}
```

## Resources Deep Dive

Resources provide structured access to information that AI applications can retrieve and provide to models as context.

### How Resources Work

Resources expose data from files, APIs, databases, or any other source that an AI needs to understand context. Applications can access this information directly and decide how to use it - whether that's selecting relevant portions, searching with embeddings, or passing it all to the model.

### Resource Types

| Type | Description | Example |
|------|-------------|---------|
| **Direct Resources** | Fixed URIs that point to specific data | `calendar://events/2024` - returns calendar availability for 2024 |
| **Resource Templates** | Dynamic URIs with parameters for flexible queries | `travel://activities/{city}/{category}` - returns activities by city and category |

### Resource Template Examples

- `travel://activities/barcelona/museums` - returns all museums in Barcelona
- `travel://activities/{city}/{category}` - returns activities by city and category

### Key Features

- **Unique URIs** (like `file:///path/to/document.md`)
- **MIME type declaration** for appropriate content handling
- **Self-documenting** with metadata (title, description, expected MIME type)
- **Discoverable** through standardized patterns

### Protocol Operations

| Method | Purpose | Returns |
|--------|---------|---------|
| `resources/list` | List available direct resources | Array of resource descriptors |
| `resources/templates/list` | Discover resource templates | Array of resource template definitions |
| `resources/read` | Retrieve resource contents | Resource data with metadata |
| `resources/subscribe` | Monitor resource changes | Subscription confirmation |


## Server Architecture

### Common Endpoints

Most MCP servers expose a single `/rpc` endpoint that handles all JSON-RPC 2.0 requests:

- **Initialize connections** with client capabilities
- **List available tools** and their schemas  
- **Execute tool calls** with parameters
- **Handle resources** (files, data sources)
- **Manage prompts** and templates

### Key Benefits

- **Standardized interface** across different server implementations
- **Type safety** through JSON Schema validation
- **User control** with consent mechanisms
- **Modular design** allowing focused functionality

## Running the Server

There are several ways to run your MCP server:

### 1. Development Mode with MCP Inspector

The easiest way to test your server is using the MCP Inspector:

```bash
mcp dev server.py
```

This runs your server locally and connects it to the MCP Inspector, a web-based tool that lets you interact with your server's tools and resources directly. This is great for testing.

### 2. Direct Execution (only needed for SSE)

You can also run the server directly:

```bash
# Method 1: Running as a Python script
python server.py

# Method 2: Using UV (recommended)
uv run server.py
```