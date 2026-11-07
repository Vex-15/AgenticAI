from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location:str) -> str:
    """get the weather of the location"""
    return "It's always rainy"

if __name__=="__main__":
    mcp.run(transport = "streamable-http")
