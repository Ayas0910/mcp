from langchain_mcp_adapters.client import MultiServerMCPClient
import sys
from pathlib import Path
import asyncio

SERVER_PATH = Path(__file__).parent/"server.py"

async def call_the_tool(session,tool_name:str,argument: dict):

    result = await session.call_tool(tool_name,argument)

    tool_output = result.content[0].text

    if result.isError:
        print("Error :", tool_output)
    else:
        print("Output :", tool_output)


client = MultiServerMCPClient(
    {
        "stdio_server":
        {
            "transport":"stdio",
            "command":sys.executable,
            "args":[str(SERVER_PATH)],
            "env":{"FASTMCP_LOG_LEVEL":"CRITICAL"}
        }
    }
)

async def main():
    async with client.session("stdio_server") as stdio:

        await call_the_tool(stdio,"divide",{"num1":10,"num2":0})

        await call_the_tool(stdio,"open_the_file",{})

asyncio.run(main())


