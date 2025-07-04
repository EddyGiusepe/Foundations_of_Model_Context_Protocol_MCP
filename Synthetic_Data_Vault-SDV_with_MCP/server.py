#! /usr/bin/env python3
"""
Senior Data Scientist.; Dr. Eddy Giusepe Chirinos Isidro

Script server.py
================
Aqui, temos um script de servidor que expõe a ferramenta usando a 
biblioteca MCP, decorando as funções usando o tooldecorador.

Com ferramentas e servidor prontos, vamos integrá-lo ao nosso Cursor IDE!
"""
from mcp.server.fastmcp import FastMCP
from tools import generate, evaluate, visualize


# Criar instância FastMCP:
mcp = FastMCP("sdv_mcp")


@mcp.tool() # <--- Registra tools para o MCP
def sdv_generate(folder_name: str) -> str:
    """Gerar dados sintéticos com base em dados reais usando o sintetizador SDV.

    Esta ferramenta lê arquivos CSV da pasta especificada, cria uma versão sintética
    desses dados e salva em uma pasta 'synthetic_data'.

    Args:
        folder_name (str): Path para a pasta contendo arquivos CSV de dados e metadata.json

    Returns:
        str: Mensagem de sucesso com informações sobre as tabelas geradas
    """
    try:
        return generate(folder_name)
    except FileNotFoundError as e:
        return f"Erro: {str(e)}"
    except RuntimeError as e:
        return f"Erro: {str(e)}"


@mcp.tool()
def sdv_evaluate(folder_name: str) -> dict:
    """Avaliar a qualidade dos dados sintéticos em comparação com dados reais.

    Esta ferramenta compara os dados sintéticos na pasta 'synthetic_data'
    com os dados reais na pasta especificada e gera métricas de qualidade.

    Args:
        folder_name (str): Path para a pasta contendo os arquivos CSV de dados originais e metadata.json

    Returns:
        dict: Resultados da avaliação incluindo pontuação geral e propriedades detalhadas
    """
    try:
        result = evaluate(folder_name)
        return result
    except FileNotFoundError as e:
        return {"error": f"Arquivo não encontrado: {str(e)}"}
    except RuntimeError as e:
        return {"error": f"Avaliação falhou: {str(e)}"}


@mcp.tool()
def sdv_visualize(
    folder_name: str,
    table_name: str,
    column_name: str,
) -> str:
    """Gerar visualização comparando dados reais e sintéticos para uma coluna específica.

    Esta ferramenta cria uma visualização comparativa entre os dados reais na pasta especificada
    e os dados sintéticos na pasta 'synthetic_data' para uma coluna específica de uma tabela.
    A visualização é salva como um arquivo PNG na pasta 'evaluation_plots'.

    Args:
        folder_name (str): Path para a pasta contendo os arquivos CSV de dados originais e metadata.json
        table_name (str): Nome da tabela a ser visualizada (deve existir nos metadados)
        column_name (str): Nome da coluna a ser visualizada dentro da tabela especificada

    Returns:
        str: Mensagem de sucesso com o caminho para a visualização salva ou mensagem de erro
    """
    try:
        return visualize(folder_name, table_name, column_name)
    except FileNotFoundError as e:
        return f"Erro: {str(e)}"
    except RuntimeError as e:
        return f"Erro: {str(e)}"


# Executar o servidor:
if __name__ == "__main__":
    mcp.run(transport="stdio")
