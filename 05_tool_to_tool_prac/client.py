from fastmcp.client.transports import PythonStdioTransport
from pathlib import Path
import sys
from fastmcp import Client
import asyncio

http_server = "http://127.0.0.1:8000/mcp"
stdio_server = PythonStdioTransport(Path(__file__).parent/"stdio_server.py",python_cmd = sys.executable)

async def main():
    async with Client(stdio_server) as stdio:
        result = await stdio.call_tool("calculate_expression",{"a":10,"b":20,"c":30})
        print(result.data)

asyncio.run(main())
