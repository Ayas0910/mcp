import asyncio
import json
import pprint

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

load_dotenv()

BRANCH = "live_mcp"
MAIN_BRANCH = "main"
repo = "live_mcp_demo"

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

    return text

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
    owner = me["login"]

    target = {"owner": owner, "repo" : repo}

    # pprint.pprint(me)
    # print()
    # pprint.pprint(tools_by_name['search_repositories'].args_schema)

    

    await call(tools_by_name["create_repository"],{
        "name": repo,
        "description":"I create this through the mcp tool",
        "private": True,
        "autoInit": True
    })

    await call(tools_by_name["create_branch"],{
        **target,
        "branch": BRANCH,
        "from_branch": MAIN_BRANCH
    })

asyncio.run(main())


    