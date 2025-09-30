from fastmcp import FastMCP

mcp = FastMCP(
    name="My MCP Server",
    host="localhost",
    port=8000
)

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http")