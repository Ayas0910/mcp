from langchain_mcp_adapters.client import MultiServerMCPClient
from pathlib import Path
import sys
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
import asyncio


http_server = "http://127.0.0.1:8000/mcp"
stdio_server = PythonStdioTransport(Path(__file__).parent/"stdio_server.py",python_cmd=sys.executable)

async def main():
    async with Client(stdio_server) as stdio, Client(http_server) as http:
        result = await stdio.call_tool("add_the_double",{"a":5,"b":10})
        print(result.data)

asyncio.run(main())



