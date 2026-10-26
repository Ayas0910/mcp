from fastmcp import FastMCP,Client

mcp = FastMCP("Stdio Server")

@mcp.tool
def double(n: int) -> int:
    """Return the double of the number."""
    return n*2

@mcp.tool
def add_the_double(a:int, b:int) -> int:
    """Add the numbers and double and return it."""
    return double(a+b)

@mcp.tool
async def sum_of_square(a:int, b:int) -> int:
    """return a*a + b*b, using the square tool of the http server."""
    async with Client("http://127.0.0.1:8000/mcp") as http:
        square_a = await http.call_tool("square",{"n":a})
        square_b = await http.call_tool("square",{"n":b})
    return square_a.data+square_b.data

mcp.run(transport="stdio")