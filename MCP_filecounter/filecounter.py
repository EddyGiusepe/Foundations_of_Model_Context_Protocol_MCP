#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Este script é um servidor MCP que conta o número de arquivos em um diretório específico.
"""
from mcp.server.fastmcp import FastMCP
import os

# Cria um servidor MCP chamado "FileCounter":
mcp = FastMCP("FileCounter")

@mcp.tool()
def count_files(directory_path: str = "/home/karinag/Documentos") -> str: # # Obtém o caminho da área de trabalho (ex., /home/karinag/Documentos)
    """Conta o número de arquivos no diretório especificado
    
    Args:
        directory_path: Caminho do diretório para contar arquivos (padrão: Desktop)
    """
    path = os.path.expanduser(directory_path)
    try:
        # Lista todos os itens no diretório, filtrando apenas arquivos:
        if not os.path.exists(path):
            return f"Erro: O diretório '{directory_path}' não existe."
        if not os.path.isdir(path):
            return f"Erro: '{directory_path}' não é um diretório."
            
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        file_count = len(files)
        return f"Existem {file_count} arquivos em '{directory_path}'."
    except Exception as e:
        return f"Erro ao contar arquivos: {str(e)}"

if __name__ == "__main__":
    mcp.run()
