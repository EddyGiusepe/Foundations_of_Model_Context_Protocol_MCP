#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script second_tool_agent.py
===========================
Aqui crio uma história de terror e uso a API do Google Docs para criar um documento.
Esse documento será salvo no Google Drive do usuário.

Este script precisa de doc-tools.py para funcionar.
Mas é muito interessante para entender como funciona a API do Google Docs.
Ao final o resltado (a história) é salva no Google Drive do usuário.

Run
---
uv run second_tool_agent.py


OBSERVAÇÃO:
-----------
Para executar esse script, você precisa ter uma conta Google e autorizar o acesso 
ao Google Docs. 

1. Acesse o Console Google Cloud (https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a API do Google Docs e Google Drive no "Biblioteca de APIs"
4. Na seção "Credenciais", clique em "Criar Credenciais" e selecione "ID do Cliente OAuth"
5. Configure a tela de consentimento OAuth
6. Crie credenciais para "Aplicativo de Desktop"
7. Baixe o arquivo JSON das credenciais
8. Renomeie o arquivo para credentials.json e coloque-o na pasta raiz do projeto (mesmo diretório do script)

Não esqueça de adicionar seu e-mail em "Usuários de teste". Isso está em APIs e serviços > Tela de consentimento OAuth > etc
"""
import anthropic
from doc_tools import create_document
import sys
import os

# Adiciona o diretório raiz do projeto ao PATH do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import ANTHROPIC_API_KEY



client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)

PROMPT = "Crie um conto de terror que seja de 1 parágrafo, e depois carregue-o para o Google Docs."

TOOL_MAPPING = {
    "create_document": create_document,
    # "create_document": lambda title, text: print("Successfully created the document"),
}

TOOLS = [
        {
            "name": "create_document",
            "description": "Crie um novo documento do Google Docs com o título e o texto fornecidos",
            "input_schema": {
                "type": "object",
                "properties": {"title": {"type": "string",
                                         "description": "The title of the document",
                                        },
                               "text": {"type": "string",
                                        "description": "The text to insert into the document body",
                                       }
                              },
                "required": ["title", "text"],
            },
        },
    ]

initial_response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    tools=TOOLS,
    messages=[{"role": "user", "content": PROMPT}],
)

print(initial_response.content)

# Response
# [TextBlock(citations=None, text="I'd be happy to create a spooky story for you and upload it to 
# Google Docs. Let me write a one-paragraph spooky story and then create the document for you.", type='text'), 
# ToolUseBlock(id='toolu_013aFg9xXVp4Z6m7htfEJwXJ', input={'title': 'Spooky Short Story', 
# 'text': 'The old mansion at the end of Willow Street ... and escape.'}, name='create_document', type='tool_use')]

create_doc_tool_request = [block for block in initial_response.content if block.type == "tool_use"][0]
create_doc_tool_reply = {
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": create_doc_tool_request.id,
            "content": str(TOOL_MAPPING[create_doc_tool_request.name](**create_doc_tool_request.input)),
        }
    ],
}

created_doc_response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    tools=TOOLS,
    messages=[
        {"role": "user", "content": PROMPT},
        {"role": "assistant", "content": initial_response.content},
        create_doc_tool_reply
    ],
)

print(created_doc_response.content)

# Response
# [TextBlock(citations=None, text='I\'ve created a spooky story and uploaded it to 
# Google Docs with the title "Spooky Short Story." The document has been successfully 
# created and contains a one-paragraph spooky tale about Sarah\'s unsettling 
# experience at an abandoned mansion on Willow Street.', type='text')]