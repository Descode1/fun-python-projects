from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Service")

@mcp.tool()
def get_weather(location):
    return f"Weather in {location}: Sunny, 25*C"

@mcp.resource("weather://{location}")
def weather_resource(location):
    return f"Weather data for {location}: Sunny, 25*C"

@mcp.prompt()
def weather_report(location):
    return f"""You are a weather reporter. Wather report for {location}?"""

if __name__ == "__main__":
    mcp.run(transport="sse", port=6969)