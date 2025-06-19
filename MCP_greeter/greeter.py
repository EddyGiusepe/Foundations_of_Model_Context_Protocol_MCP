#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Este é um servidor MCP que retorna uma mensagem de boas-vindas.
"""
from mcp.server.fastmcp import FastMCP

# Cria um servidor MCP nomeado "Greeter"
mcp = FastMCP("Greeter")


@mcp.tool()
def greet() -> str:
    """Retorna esta mensagem de boas-vindas, quando cumprimentado com "Olá", "Oi" ou "Hey"."""
    return "Olá Eddy Giusepe, Bem-vindo ao mundo dos MCPs!"


if __name__ == "__main__":
    mcp.run()
