from fastmcp import FastMCP,Client

mcp = FastMCP("stdio_server")

@mcp.tool
async def calculate_expression(a:int,b:int,c:int)->int:
    "It calculate all the three numbers and return the result"
    async with Client("http://127.0.0.1:8000/mcp") as http:
        result_add = await http.call_tool("add",{"a":a,"b":b})
        result_multiply = await http.call_tool("multiply",{"a":a,"b":b})
        return result_add.data + result_multiply.data

mcp.run(transport = "stdio")