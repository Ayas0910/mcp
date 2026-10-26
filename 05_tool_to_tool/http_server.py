from fastmcp import FastMCP

mcp = FastMCP("HTTP Server")

@mcp.tool
def square(n: int) -> int:
    """Return the multiple of the number."""
    return n*n

mcp.run(transport="http",host="127.0.0.1",port=8001)