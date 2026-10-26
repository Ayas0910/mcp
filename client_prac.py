from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import asyncio
from pprint import pprint


load_dotenv()

async def main():

    #pick the right tool
    client = MultiServerMCPClient(
        {
            "server_configuration":{
                "transport":"stdio",
                "command":sys.executable,
                "args":["server_prac.py"]
            }
        }
    )

    tools = await client.get_tools()

    llm = ChatOpenAI(model = "gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools = tools)

    messages = [(HumanMessage(content = "Hello, My name is Ayas"))]

    response = await llm_with_tools.ainvoke(messages)

    pprint(response.model_dump())

    #execute the rigth tool

    tool_execute = {tool.name: tool for tool in tools}

    for tool in response.tool_calls:
        response_tool = tool_execute[tool["name"]]
        result = await response_tool.ainvoke(tool['args'])
        print(result[0]["text"])

asyncio.run(main())

 