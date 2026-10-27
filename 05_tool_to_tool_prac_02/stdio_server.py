from fastmcp import FastMCP,Client

mcp = FastMCP("stdio_server")


@mcp.tool
def double(n:int) -> int:
    """It multiply the n into 2 and return the number"""
    return n*2

@mcp.tool
async def square_using_http(n:int) ->int:
    """It calls the http server square method"""
    async with Client("http://127.0.0.1:8000/mcp") as http:
        result = await http.call_tool("square",{"a":n})
        return result.data


mcp.run(transport="stdio",show_banner=True)