from mcp.server.fastmcp import FastMCP

# Create an MCP server named "Greeter"
mcp = FastMCP("Greeter")

@mcp.tool()
def greet() -> str:
    """Return this welcome message, when greeted with "Hi", "Hey" or "Hello"."""
    return "Olá Eddy Giusepe, bem-vindo ao mundo MCPs!"




if __name__ == "__main__":
    mcp.run()