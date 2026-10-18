from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient 
import sys
import asyncio

#import api key
load_dotenv()


async def main():
    client = MultiServerMCPClient(
    {
        "greeting":{
            "transport":"stdio",
            "command":sys.executable,
            "args":["server.py"]
        }
    }
)

    tools = await client.get_tools()
    print(tools)

asyncio.run(main())
