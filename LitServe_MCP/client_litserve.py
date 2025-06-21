#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Link de estudo --> https://lightning.ai/docs/litserve/features/mcp

client_litserve.py
==================
Cliente para interagir com o servidor de análise de sentimento (server.py).
Este cliente usa a API do Anthropic para processar consultas e interagir com o servidor.

Run
===
uv run client_litserve.py /home/karinag/1_GitHub/Foundations_of_Model_Context_Protocol_MCP/LitServe_MCP/server.py
"""
import asyncio
import httpx
from anthropic import Anthropic
import sys
import os
import json

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Se tiver um arquivo de configuração com chave da API:
try:
    from config.settings import ANTHROPIC_API_KEY
except ImportError:
    ANTHROPIC_API_KEY = "<SUA_CHAVE_DE_API_AQUI>"

# URL do servidor
SERVER_URL = "http://localhost:8000"


class SentimentClient:
    def __init__(self):
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.client = httpx.AsyncClient()

    async def check_server_connection(self):
        """Verifica se o servidor está disponível"""
        try:
            response = await self.client.get(f"{SERVER_URL}/")
            if response.status_code == 200:
                print("\n🤗 Conectado ao servidor de análise de sentimento 🤗!")
                return True
            else:
                print(f"\nErro ao conectar ao servidor: {response.status_code}")
                return False
        except httpx.ConnectError:
            print("\nNão foi possível conectar ao servidor. Verifique se o servidor está rodando.")
            return False

    async def analyze_sentiment(self, text):
        """Envia texto para análise de sentimento ao servidor"""
        try:
            response = await self.client.post(
                f"{SERVER_URL}/predict",
                json={"input": text}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Erro {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    async def process_query(self, query: str) -> str:
        """Processa uma consulta para análise de sentimento"""
        # Envia o texto para análise:
        result = await self.analyze_sentiment(query)
        
        if "error" in result:
            return f"Erro ao analisar sentimento: {result['error']}"
        
        # Usa o Claude para explicar o resultado em linguagem natural
        messages = [
            {"role": "user",
             "content": f"""Explique o resultado desta análise de sentimento de forma clara 
                            e concisa e em linguagem natural: {json.dumps(result)}"""}
        ]
        
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=messages,
            temperature=0.1,
        )
        
        return response.content[0].text

    async def chat_loop(self):
        """Executa um loop de chat interativo para análise de sentimentos"""
        print("\n🔍 Cliente de Análise de Sentimentos Iniciado! 🔍")
        print("Digite textos para análise de sentimento.")
        print("Exemplos:")
        print("- Estou muito feliz com este novo produto!")
        print("- A experiência foi terrível e não recomendo.")
        print("- O filme foi interessante, mas poderia ser melhor.")
        print("Digite 'quit' para sair.")

        while True:
            try:
                query = input("\n✨ Digite o texto para análise 🧐: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nErro: {str(e)}")

    async def cleanup(self):
        """Limpa recursos"""
        await self.client.aclose()


async def main():
    client = SentimentClient()
    try:
        if await client.check_server_connection():
            await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
