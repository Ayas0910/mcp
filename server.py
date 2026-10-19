from fastmcp import FastMCP


mcp = FastMCP("FirstMCPServer")

@mcp.tool
def greet(name: str) -> str:
    """This is the greet tool. it get the name and greet the user."""
    return f"Hello {name} Welcome to MCP Server. This is a first server I am creating right now."

mcp.run(transport = "stdio")



