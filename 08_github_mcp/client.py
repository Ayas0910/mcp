import asyncio
import json
import pprint

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

load_dotenv()

async def call(tool,args):

    result = await tool.ainvoke(args)

    text = result[0]["text"]

    try:
        text = json.loads(text)
    except json.JSONDecodeError:
        pass

    print(f"\n---{tool.name}---\n{text}")

    if isinstance(text,str) and text.startswith("failed"):
        raise RuntimeError(f"{tool.name} {text}")

    return text;

async def main():

    client = MultiServerMCPClient(
        {
            "github":
            {
                "transport":"streamable_http",
                "url": "https://api.githubcopilot.com/mcp/",
                "headers":{
                    "Authorization": f'Bearer {os.environ["github_personal_access_token"]}'
                }
            }
        }
    )

    tools = await client.get_tools()
    tools_by_name = {tool.name: tool for tool in tools}
    # pprint.pprint(tools_by_name)

    me = await call(tools_by_name["get_me"],{})

    # pprint.pprint(me)
    # print()
    # pprint.pprint(tools_by_name['search_repositories'].args_schema)

    repo = "live_mcp_demo"

    await call(tools_by_name["create_repository"],{
        "name": repo,
        "description":"I create this through the mcp tool",
        "private": True,
        "autoInit": True
    })

asyncio.run(main())


    