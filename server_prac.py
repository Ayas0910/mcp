from fastmcp import FastMCP

mcp = FastMCP("FirstMCPServer")

@mcp.tool
def greet(name: str) -> str:
    """This is a greet tool. It get the name from the user and returns a greeting message."""
    return f"Hello {name}, welcome to the MCP Server."

mcp.run(transport="stdio", show_banner = True)