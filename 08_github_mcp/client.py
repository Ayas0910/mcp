import json

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
                    "Authorization": f"Bearer {os.environ["github_personal_access_token"]}"
                }
            }
        }
    )

    