#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script first_tool.py
====================
Neste script, veremos como o LLM pode usar ferramentas para resolver um problema.

Run
===
uv run first_tool.py
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

# Neste caso, nós damos ao LLM algumas FERRAMENTAS que ele pode usar para encontrar a resposta:
def subtract(a: int, b: int) -> int:
    return a-b

def sqrt(num: int) -> float:
    return num**0.5

TOOL_MAPPING = {
    "subtract": subtract,
    "sqrt": sqrt,
}

TOOLS = [
        {
            "name": "subtract",
            "description": "Calcula a diferença entre `a` e `b`",
            "input_schema": {
                "type": "object",
                "properties": {"a": {"type": "number",
                                     "description": "O primeiro operando",
                                    },
                               "b": {"type": "number",
                                     "description": "O segundo operando; o número a ser subtraído",
                                     }
                              },
                "required": ["a", "b"],
            },
        },
        {
            "name": "sqrt",
            "description": "Encontra a raiz quadrada de um número inteiro",
            "input_schema": {
                "type": "object",
                "properties": {"num": {"type": "number",
                                       "description": "O operando para encontrar a raiz quadrada",
                                      },
                              },
                "required": ["num"],
            },
        }
    ]

initial_response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    tools=TOOLS,
    messages=[{"role": "user", "content": PROMPT}],
)

print(initial_response.content)
# Response
# [TextBlock(citations=None, text='Vou calcular a diferença entre 316043 e 201122, e depois encontrar a raiz quadrada do resultado.', type='text'), 
# ToolUseBlock(id='toolu_01N3c4Qr2tF7AvJR84Cw2bsD', input={'a': 316043, 'b': 201122}, name='subtract', type='tool_use')]

subract_tool_request = [block for block in initial_response.content if block.type == "tool_use"][0]
subract_tool_reply = {
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": subract_tool_request.id,
            "content": str(TOOL_MAPPING[subract_tool_request.name](**subract_tool_request.input)),
        }
    ],
}

intermediate_response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    tools=TOOLS,
    messages=[
        {"role": "user", "content": PROMPT},
        {"role": "assistant", "content": initial_response.content},
        subract_tool_reply
    ],
)

print(intermediate_response.content)

# Response
# [TextBlock(citations=None, text='Agora vou encontrar a raiz quadrada desse resultado:', type='text'), ToolUseBlock(id='toolu_01EN61STvR5jXfJtryzhjkEz', input={'num': 114921}, name='sqrt', type='tool_use')]

sqrt_tool_request = [block for block in intermediate_response.content if block.type == "tool_use"][0]
sqrt_tool_reply = {
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": sqrt_tool_request.id,
            "content": str(TOOL_MAPPING[sqrt_tool_request.name](**sqrt_tool_request.input)),
        }
    ],
}

final_response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    tools=TOOLS,
    messages=[
        {"role": "user", "content": PROMPT},
        {"role": "assistant", "content": initial_response.content},
        subract_tool_reply,
        {"role": "assistant", "content": intermediate_response.content},
        sqrt_tool_reply,
    ],
)

print("\nResposta final:")
print(final_response.content) # [TextBlock(citations=None, text='339.0', type='text')]
