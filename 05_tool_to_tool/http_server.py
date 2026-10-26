from fastmcp import FastMCP,Client
from pathlib import Path
from fastmcp.client.transports import PythonStdioTransport


mcp = FastMCP("HTTP Server")

@mcp.tool
def square(n: int) -> int:
    """Return the multiple of the number."""
    return n*n

@mcp.tool
async def double_and_square(n: int) -> int:
    """Return the double and square of the number."""
    stdio_server = PythonStdioTransport(Path(__file__).parent/"stdio_server.py")
    async with Client(stdio_server) as stdio:
        double_n = await stdio.call_tool("double",{"n":n})
        return square(double_n.data)

mcp.run(transport="http",host="127.0.0.1",port=8001)