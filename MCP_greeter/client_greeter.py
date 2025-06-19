#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Cliente para interagir com o servidor Greeter MCP.

Run
===
uv run client_greeter.py /home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/MCP_greeter/greeter.py
"""
import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis de ambiente do arquivo .env


class GreeterClient:
    def __init__(self):
        # Inicia objetos de session e client:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        """Conecta ao servidor MCP Greeter

        Args:
            server_script_path: Caminho para o script do servidor greeter.py
        """
        if not server_script_path.endswith(".py"):
            raise ValueError("O script do servidor deve ser um arquivo .py")

        server_params = StdioServerParameters(
            command="python", args=[server_script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # Lista ferramentas disponíveis:
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConectado ao servidor com ferramentas:", [tool.name for tool in tools])

    async def process_greeting(self, greeting: str) -> str:
        """Processa uma saudação usando a ferramenta greet diretamente"""
        greeting_lower = greeting.lower()

        # Verifica se a entrada é uma das saudações esperadas
        if greeting_lower in ["olá", "oi", "hey"]:
            # Chama diretamente a ferramenta greet
            result = await self.session.call_tool("greet", {})
            print(f"Chamando ferramenta greet: {result.content}")
            return result.content[0].text
        else:
            return "Por favor, use 'Olá', 'Oi' ou 'Hey' para receber uma saudação."

    async def chat_loop(self):
        """Executa um loop de chat interativo"""
        print("\n🤗 Greeter MCP Client Iniciado 🤗!")
        print("Digite 'Olá', 'Oi' ou 'Hey' para receber uma saudação")
        print("Digite 'quit' para sair.")

        while True:
            try:
                greeting = input("\nDigite sua saudação: ").strip()

                if greeting.lower() == "quit":
                    break

                response = await self.process_greeting(greeting)
                print("\n" + response)

            except Exception as e:
                print(f"\nErro: {str(e)}")

    async def cleanup(self):
        """Limpa recursos"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Uso: python client_greeter.py <caminho_para_greeter.py>")
        sys.exit(1)

    client = GreeterClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
