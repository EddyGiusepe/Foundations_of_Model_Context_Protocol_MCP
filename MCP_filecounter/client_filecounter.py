#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Cliente para interagir com o servidor FileCounter MCP.
Este cliente usa a API do Anthropic para gerar respostas mais naturais e claras.
Basicamente, o usuário pode perguntar, DE FORMA NATURAL, quantos arquivos tem 
em um determinado diretório.

Run
===
uv run client_filecounter.py /home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/MCP_filecounter/filecounter.py
"""
import asyncio
import sys
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


class FileCounterClient:
    def __init__(self):
        # Inicia objetos de session e client:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

    async def connect_to_server(self, server_script_path: str):
        """Conecta ao servidor MCP FileCounter

        Args:
            server_script_path: Caminho para o script do servidor filecounter.py
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

    async def count_files(self, directory_path: str = "/home/karinag/Documentos") -> str:
        """Chama a ferramenta count_files para contar arquivos
        
        Args:
            directory_path: Caminho do diretório para contar arquivos
        """
        try:
            # Chama a ferramenta count_files
            result = await self.session.call_tool("count_files", {"directory_path": directory_path})
            print(f"Chamando ferramenta count_files: {result.content}")
            return result.content[0].text
        except Exception as e:
            return f"Erro ao contar arquivos: {str(e)}"

    async def chat_loop(self):
        """Executa um loop de chat interativo com IA"""
        print("\n📁 FileCounter MCP Client com IA Iniciado 📁!")
        print("Exemplos de comandos:")
        print("- 'Quantos arquivos tem na pasta ~/Documentos?'")
        print("- 'Contar arquivos em ~/Desktop'")
        print("- 'Analise os arquivos da pasta /home/user'")
        print("Digite 'quit' para sair.")

        while True:
            try:
                user_input = input("\nDigite seu comando: ").strip()

                if user_input.lower() == "quit":
                    break

                # Usar IA para interpretar o comando
                response = await self.process_with_ai(user_input)
                print("\n" + response)

            except Exception as e:
                print(f"\nErro: {str(e)}")

    async def cleanup(self):
        """Limpa recursos"""
        await self.exit_stack.aclose()

    async def process_with_ai(self, user_input: str) -> str:
        """Processa entrada do usuário usando IA para interpretar comandos"""
        try:
            # Usar IA para extrair o caminho do diretório
            messages = [
                {
                    "role": "user",
                    "content": f"""
                    Analise este comando do usuário: "{user_input}"
                    
                    Se o usuário quer contar arquivos em um diretório, extraia o caminho.
                    Se não especificar caminho, use "/home/karina/Documentos" como padrão.
                    
                    Responda apenas com o caminho do diretório, nada mais.
                    Exemplos:
                    - "Quantos arquivos tem em ~/Documentos?" → ~/Documentos
                    - "Contar arquivos" → ~/Desktop
                    - "Analise /home/user/pasta" → /home/user/pasta
                    """
                }
            ]
            
            ai_response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=messages
            )
            
            directory_path = ai_response.content[0].text.strip()
            
            # Contar arquivos no diretório extraído:
            count_result = await self.count_files(directory_path)
            
            # Usar IA para gerar resposta mais natural:
            final_messages = [
                {
                    "role": "user", 
                    "content": f"""
                    O usuário perguntou: "{user_input}"
                    Resultado da contagem: {count_result}
                    
                    Gere uma resposta natural e clara em português brasileiro.
                    """
                }
            ]
            
            final_response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=final_messages
            )
            
            return final_response.content[0].text
            
        except Exception as e:
            return f"Erro ao processar comando: {str(e)}"


async def main():
    if len(sys.argv) < 2:
        print("Uso: python client_filecounter.py <caminho_para_filecounter.py>")
        sys.exit(1)

    client = FileCounterClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
