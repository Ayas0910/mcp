from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pathlib import Path

mcp = FastMCP("Stdio_server",mask_error_details = True)

@mcp.tool
def divide(num1: int, num2: int) -> int:
    """We try the divide the two numbers"""
    if num2 == 0:
        raise ToolError("Please give the valid number for the num2")
    else:
        return num1 // num2

@mcp.tool
def open_the_file():
    """Open the current directory file"""
    return open(Path(__file__).parent/"password.txt").read()

mcp.run(transport = "stdio", show_banner = True)