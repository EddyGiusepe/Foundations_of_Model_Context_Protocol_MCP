from mcp.server.fastmcp import FastMCP

# Cria um servidor MCP nomeado "Greeter"
mcp = FastMCP("Greeter")

@mcp.tool()
def greet() -> str:
    """Retorna esta mensagem de boas-vindas, quando cumprimentado com "Olá", "Oi" ou "Hey"."""
    return "Olá Eddy Giusepe, Bem-vindo ao mundo dos MCPs!"

if __name__ == "__main__":
    mcp.run()
