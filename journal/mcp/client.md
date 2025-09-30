### Client-Side Implementation (with Standard I/O)

Now, let's see how to create a client that uses our server:

```python
import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server.py"],  # Arguments to the command
    )

    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
```

This client:

1. Creates a connection to our server via stdio
2. Establishes an MCP session
3. Lists available tools
4. Calls the `add` tool with arguments

### Client-Side Implementation (with Server-Sent Events)

Here's how to connect to your server with SSE:

```python
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Client-Side Implementation (with Streamable HTTP) 

> **Note**: Streamable HTTP transport was introduced on **March 24, 2025** and is now the **recommended approach for production deployments**, superseding SSE transport. [Learn more in the official documentation](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).

**Why Streamable HTTP?**

Streamable HTTP offers several advantages over SSE:
- **Better Performance**: 3-5x improvement under high concurrency
- **Simplified Architecture**: Single endpoint instead of separate HTTP + SSE endpoints
- **Enhanced Scalability**: Better support for multi-node deployments
- **Modern Standards**: Built on current HTTP streaming standards

**How It Works:**

Streamable HTTP uses a single HTTP endpoint (`/mcp`) that supports both stateful and stateless operation modes. Unlike SSE which requires maintaining separate endpoints, Streamable HTTP provides a unified interface for all MCP communication.

Here's how to connect using the new Streamable HTTP transport:

```python
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    # Connect to the server using Streamable HTTP
    async with streamablehttp_client("http://localhost:8050/mcp") as (read_stream, write_stream, get_session_id):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Key Differences:**

| Feature | stdio | SSE | Streamable HTTP |
|---------|-------|-----|-----------------|
| **Endpoint** | N/A (local) | `/sse` | `/mcp` |
| **Return Values** | `(read, write)` | `(read, write)` | `(read, write, get_session_id)` |
| **Architecture** | Bidirectional streams | Separate HTTP + SSE | Unified HTTP streaming |
| **Best For** | Development/local | Development/legacy | **Production** |

### Which Approach Should You Choose?

- **Use stdio** if your client and server will be running in the same process or if you're starting the server process directly from your client.
- **Use Streamable HTTP** for production deployments where you need the best performance and scalability.
- **Use SSE** for development or when working with older MCP implementations that don't yet support Streamable HTTP.

For most production backend integrations, the **Streamable HTTP** approach offers the best performance and modern architecture, while stdio might be simpler for development or tightly coupled systems.