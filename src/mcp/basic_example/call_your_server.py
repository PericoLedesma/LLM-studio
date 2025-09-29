import asyncio
from fastmcp import Client

# # In-memory server (ideal for testing)
# server = FastMCP("TestServer")
# client = Client(server)

# # Local Python script
# client = Client("my_mcp_server.py")



# HTTP server
client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        # result = await client.call_tool("greet", {"name": name})
        # print(result)


        # First, get the list of available tools
        tools = await client.list_tools()
        print("\n🔧 Available Tools:")
        print("=" * 50)
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool.name}")
            if hasattr(tool, 'description') and tool.description:
                print(f"   📝 {tool.description}")
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                print(f"   📋 Parameters: {list(tool.inputSchema.get('properties', {}).keys())}")
            print()

        print("=" * 50)
        # Then call the greet tool
        result = await client.call_tool("greet", {"name": "Ford"})
        print("Greeting result:", result)


asyncio.run(call_tool("Ford"))