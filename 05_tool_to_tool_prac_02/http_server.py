from fastmcp import FastMCP,Client
from fastmcp.client.transports import PythonStdioTransport
from pathlib import Path
import sys


mcp = FastMCP("http_server")

@mcp.tool
def square(a: int) -> int:
    """multiply the number with the same number"""
    return a*a

@mcp.tool
async def double_using_stdio(n: int)->int:
    """I using the stido server double method"""
    stdio_server = PythonStdioTransport(Path(__file__).parent/"stdio_server.py",python_cmd = sys.executable)
    async with Client(stdio_server) as stdio:
        result = await stdio.call_tool("double",{"n":n})
        return result.data



mcp.run(transport="http",host="127.0.0.1",port = 8000)