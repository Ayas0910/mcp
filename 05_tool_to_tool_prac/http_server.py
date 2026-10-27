from fastmcp import FastMCP

mcp = FastMCP("http_server")

@mcp.tool
def add(a:int,b:int)->int:
    "It add the two numbers and return the result"
    return a+b

@mcp.tool
def multiply(a:int,b:int)->int:
    "It multiply the two numbers and return the result"
    return a*b

mcp.run(transport= "http",host="127.0.0.1",port=8000)