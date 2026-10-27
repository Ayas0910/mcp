from fastmcp import Client
import asyncio
from fastmcp.client.transports import PythonStdioTransport
from pathlib import Path
import sys

http_server = "http://127.0.0.1:8000/mcp"

stdio_server = PythonStdioTransport(Path(__file__).parent/"stdio_server.py",python_cmd = sys.executable)

async def main():
    async with Client(stdio_server) as stdio, Client(http_server) as http:
        result_stdio =await http.call_tool("double_using_stdio",{"n":1})
        result_http =await stdio.call_tool("square_using_http",{"n":2})
        print(f"1:{result_stdio.data}")
        print(f"2:{result_http.data}")  

asyncio.run(main())