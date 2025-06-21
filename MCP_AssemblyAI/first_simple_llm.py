#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script first_simple_llm.py
==========================
Aqui veremos a limitação estocástica do LLM e a falta de confiabilidade em
certos cenários.

Run
===
uv run first_simple_llm.py
"""
import anthropic
import sys
import os

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import ANTHROPIC_API_KEY

client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)

# Nós damos esta conta para o LLM, onde a resposta verdadeira é 339:
PROMPT = (
    "Encontrar o valor de 201122 removido de 316043 e depois encontrar a raiz quadrada do resultado. "
    "Retornar este valor **apenas** com nenhuma outra palavra."
)


response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    temperature=0.0,
    max_tokens=1024,
    #stream=True,
    messages=[{"role": "user", "content": PROMPT}],
)

print(response.content[0].text) # [TextBlock(citations=None, text='400', type='text')]
