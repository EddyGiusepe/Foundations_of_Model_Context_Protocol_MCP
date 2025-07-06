#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

client_sdv.py
============
Cliente para interagir com o servidor SDV que gera dados sintéticos.
Este cliente permite fazer consultas para gerar dados sintéticos com base
em dados existentes.

Run
===
uv run client_sdv.py /home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/Synthetic_Data_Vault-SDV_with_MCP/server.py
"""
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
import sys
import os

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import ANTHROPIC_API_KEY


class SDVClient:
    def __init__(self):
        # Inicia session e client objects:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def connect_to_server(self, server_script_path: str):
        """Connecta ao servidor SDV MCP

        Args:
            server_script_path: Caminho para o script do servidor (.py ou .js)
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("O script do servidor deve ser um arquivo .py ou .js")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
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

    async def process_query(self, query: str) -> str:
        """Processa uma consulta usando Claude e ferramentas disponíveis"""
        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        # Chamada API Claude inicial:
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
            temperature=0.1
        )

        # Processa resposta e lida com chamadas de ferramenta:
        final_text = []

        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # Executa chamada de ferramenta:
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(
                    f"[Chamando ferramenta {tool_name} com args {tool_args}]"
                )

                # Continue a conversa com os resultados da ferramenta:
                if hasattr(content, "text") and content.text:
                    messages.append({"role": "assistant", "content": content.text})
                messages.append({"role": "user", "content": result.content})

                # Obtém próxima resposta do Claude:
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Executa um loop de chat interativo"""
        print("\n🤖 SDV Client Iniciado 🤖!")
        print("Utilize para gerar dados sintéticos")
        print("Digite suas consultas ou 'quit' para sair.")
        print("\nExemplo: Gerar dados sintéticos para os dados presentes na pasta '/home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/Synthetic_Data_Vault-SDV_with_MCP/data'")
        print("\nExemplo: Avalie os dados sintéticos que foram gerados para a pasta de dados real localizada em '/home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/Synthetic_Data_Vault-SDV_with_MCP/data'")
        print("\nExemplo: Visualize a coluna 'amenities_fee' da tabela 'guests' dos dados localizados em '/home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/Synthetic_Data_Vault-SDV_with_MCP/synthetic_data' e compare a distribuição dos dados sintéticos com a dos dados reais para esta coluna específica.")

        while True:
            try:
                query = input("\nDigite sua consulta: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nErro: {str(e)}")

    async def cleanup(self):
        """Limpa recursos"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Uso: python client_sdv.py <caminho_para_o_script_do_servidor>")
        sys.exit(1)

    client = SDVClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())


