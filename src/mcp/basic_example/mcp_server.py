from fastmcp import FastMCP
from typing import Annotated

mcp = FastMCP(
    name="My MCP Server",
    host="localhost",
    port=8000
)


@mcp.tool
def greet(
        name: Annotated[str, "The name of the person to greet"]
) -> str:
    """
    Greet a person by name with a friendly hello message.

    This tool generates a personalized greeting for the given name.
    """
    return f"Hello, {name}!"


@mcp.tool
def add_numbers(
        a: Annotated[int, "The first number to add"],
        b: Annotated[int, "The second number to add"]
) -> int:
    """
    Add two numbers together and return the sum.

    This tool performs basic addition of two integer values.
    """
    return a + b

if __name__ == "__main__":
    mcp.run(transport="http")