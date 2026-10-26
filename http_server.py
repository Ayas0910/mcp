from fastmcp import FastMCP

mcp = FastMCP("FirstMCPHttpServer")

mcp.run(transport="http",host="127.0.0.1",port=8000)

