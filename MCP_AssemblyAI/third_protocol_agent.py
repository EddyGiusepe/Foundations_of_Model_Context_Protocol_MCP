#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Run
===

uv run third_protocol_agent.py /home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/MCP_AssemblyAI/gdocs_mcp_server.py

O MCP é importante
==================
Ele padroniza a maneira como os agentes de AI irão interagir com serviços externos.
Isso é importante porque nos permite construir sistemas que são interoperáveis e combináveis.

Em particular, o MCP transfere a responsabilidade de fazer os agentes de AI interagirem com 
os serviços para os provedores de serviços. 
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


class MCPClient:
    def __init__(self):
        # Inicialização de objetos de sessão e cliente:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def connect_to_server(self, server_script_path: str):
        """Conectar-se a um servidor MCP

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

        # Listar ferramentas disponíveis:
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConectado ao servidor com ferramentas:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Processar uma consulta usando Claude e ferramentas disponíveis"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # Chamada inicial da API Claude:
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        # Processar resposta e lidar com chamadas de ferramenta:
        final_text = []

        assistant_message_content = []
        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Executar chamada de ferramenta:
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Chamando ferramenta {tool_name} com args {tool_args}]")

                assistant_message_content.append(content)
                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                # Obter próxima resposta da API Claude:
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                    tools=available_tools
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Executar um loop de chat interativo"""
        print("\n🤖 MCP Client Iniciado 🤖!")
        print("👉 Este CLIENT pede para o servidor criar um documento no Google Drive.")
        print("Exemplos:")
        print("- Crie um conto de terror que seja de um parágrafo, e depois carregue-o para o Google Drive.")
        print("- Crie uma história de apenas um parágrafo sobre o Físico e Cientista de Dados Dr. Eddy Giusepe.")
        print("- Crie uma história de terror, de apenas um parágrafo, baseado no Universo. O nome do arquivo: 'O lado terrorífico do Universo'")
        print("- Crie um documento, de apenas um parágrafo, sobre a importância da IA no mundo. O nome do arquivo: 'A IA e sua importância no mundo'")
        print("\n")
        print("Digite suas consultas ou 'quit' para sair.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Limpar recursos"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Uso: python client.py <caminho_para_o_script_do_servidor>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys

    asyncio.run(main())