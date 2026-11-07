from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

load_dotenv()

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

    