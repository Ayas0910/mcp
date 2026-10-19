from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

import sys
from pathlib import Path
import asyncio

load_dotenv()

SERVER_PATH = Path(__file__).parent / "server.py"

async def main():
    client = MultiServerMCPClient({
        'greeting': {
            'transport':'stdio',
            'command': sys.executable,
            "args": [str(SERVER_PATH)]
        }
    })

    tools = await client.get_tools() # to get the tools list

    # For LLM
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools=tools)

    messages = [HumanMessage(content="Print Akshay in unique way default times")]

    response =  await llm_with_tools.ainvoke(messages)
    print(response)
    

asyncio.run(main())


