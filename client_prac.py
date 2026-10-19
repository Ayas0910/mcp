from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import sys
import asyncio

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "greeting":{
                "transport": "stdio",
                "command":sys.executable,
                "args":["server_prac.py"]
            }
        }
    )

    tools = await client.get_tools()

    print(tools)


asyncio.run(main())