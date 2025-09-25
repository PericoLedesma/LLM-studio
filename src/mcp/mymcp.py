# from mcp.server.fastmcp import FastMCP

from fastmcp import FastMCP


from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


mcp = FastMCP(name="Notes App")

@mcp.tool()
def get_my_notes() -> str:
    """Get all notes for a user"""
    return "no notes"

@mcp.tool()
def add_note(content: str) -> str:
    """Add a note for a user"""
    return f"added note: {content}"


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )




