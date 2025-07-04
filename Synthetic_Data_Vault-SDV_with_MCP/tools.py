#! /usr/bin/env python3
"""
Senior Data Scientist.; Dr. Eddy Giusepe Chirinos Isidro

Script tools.py
===============
Este script contém ferramentas para gerar dados sintéticos, avaliar a qualidade desses dados e visualizá-los.
"""
import os
import pandas as pd
from sdv.io.local import CSVHandler
from sdv.metadata import Metadata
from sdv.multi_table import HMASynthesizer
from sdv.evaluation.multi_table import evaluate_quality, get_column_plot


# Tool 1: Data Generation: Esta ferramenta cria dados sintéticos a partir de dados reais 
                         # usando o sintetizador SDV. A SDV oferece uma variedade de sintetizadores,
                         # cada um utilizando algoritmos diferentes para produzir dados sintéticos.
def generate(folder_name: str):
    """Gerar dados sintéticos a partir de dados reais usando o sintetizador SDV."""
    # Verificar se a pasta de dados existe:
    if not os.path.exists(folder_name):
        raise FileNotFoundError(f"A pasta {folder_name} não existe.")

    # Verificar se o arquivo de metadados existe:
    metadata_file = os.path.join(folder_name, "metadata.json")
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"O arquivo de metadados {metadata_file} não existe.")

    try:
        # Carregar arquivos CSV de dados da pasta especificada:
        connector = CSVHandler()
        data = connector.read(folder_name=folder_name)

        # Carregar metadados:
        metadata = Metadata.load_from_json(metadata_file)

        # Criar e treinar o sintetizador:
        synthesizer = HMASynthesizer(metadata)
        synthesizer.fit(data)

        # Gerar dados sintéticos:
        synthetic_data = synthesizer.sample(scale=1)

        # Salvar dados sintéticos em arquivos CSV:
        os.makedirs("synthetic_data", exist_ok=True)
        for table_name, df in synthetic_data.items():
            output_file = os.path.join("synthetic_data", f"{table_name}.csv")
            df.to_csv(output_file, index=False)

        return f"Dados gerados com sucesso e salvos na pasta 'synthetic_data' com {len(synthetic_data)} tabelas nomeadas como {list(synthetic_data.keys())} arquivos CSV."

    # Tratamento de exceções durante a geração de dados:
    except Exception as e:
        raise RuntimeError(f"Ocorreu um erro ao gerar dados sintéticos: {e}")

# Tool 2: Data Evaluation: Esta ferramenta avalia a qualidade de dados sintéticos em comparação com dados reais.
                         # Avaliaremos a similaridade estatística para determinar quais padrões de dados reais são capturados pelos dados sintéticos.
def evaluate(folder_name: str):
    """Avaliar a qualidade de dados sintéticos em comparação com dados reais."""
    # Verificar se as pastas de dados reais e sintéticos existem:
    if not os.path.exists(folder_name):
        raise FileNotFoundError(f"A pasta de dados reais {folder_name} não existe.")
    if not os.path.exists("synthetic_data"):
        raise FileNotFoundError(
            f"A pasta de dados sintéticos não foi encontrada. Por favor, gere dados sintéticos primeiro usando o método SDV generate."
        )

    # Verificar se o arquivo de metadados existe:
    metadata_file = os.path.join(folder_name, "metadata.json")
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"O arquivo de metadados {metadata_file} não existe.")

    try:
        # Carregar metadados:
        metadata = Metadata.load_from_json(metadata_file)

        # Obter a lista de tabelas a partir dos metadados:
        table_names = metadata.tables

        # Criar dicionários de dados:
        real_data_dict = {}
        synthetic_data_dict = {}

        # Carregar cada tabela a partir de arquivos CSV:
        for table_name in table_names:
            real_path = os.path.join(folder_name, f"{table_name}.csv")
            synthetic_path = os.path.join("synthetic_data", f"{table_name}.csv")

            if not os.path.exists(real_path):
                raise FileNotFoundError(f"Arquivo de dados reais não encontrado: {real_path}")
            if not os.path.exists(synthetic_path):
                raise FileNotFoundError(
                    f"Arquivo de dados sintéticos não encontrado: {synthetic_path}"
                )

            real_data_dict[table_name] = pd.read_csv(real_path)
            synthetic_data_dict[table_name] = pd.read_csv(synthetic_path)

        # Executar avaliação:
        quality_report = evaluate_quality(
            real_data=real_data_dict,
            synthetic_data=synthetic_data_dict,
            metadata=metadata,
            verbose=False,
        )

        # Obter a pontuação geral e as propriedades:
        overall_score = quality_report.get_score()
        properties_df = quality_report.get_properties()
        properties = properties_df.to_dict(orient="records")

        # Retornar métricas:
        return {"Overall Score": overall_score, "Properties": properties}

    # Tratamento de exceções durante a avaliação:
    except Exception as e:
        raise RuntimeError(f"Ocorreu um erro durante a avaliação: {e}")

# Tool 3: Data Visualization: Esta ferramenta gera uma visualização para comparar dados reais e sintéticos para uma coluna específica.
                            # Use esta função para visualizar uma coluna real ao lado de sua coluna sintética correspondente.
def visualize(
    folder_name: str,
    table_name: str,
    column_name: str,
    visualization_folder: str = "evaluation_plots",
):
    """Gerar visualização comparando dados reais e sintéticos para uma coluna específica."""
    # Verificar se as pastas de dados reais e sintéticos existem:
    if not os.path.exists(folder_name):
        raise FileNotFoundError(f"A pasta de dados reais {folder_name} não existe.")
    if not os.path.exists("synthetic_data"):
        raise FileNotFoundError(
            "A pasta de dados sintéticos não foi encontrada. Por favor, gere dados sintéticos primeiro."
        )

    # Verificar se o arquivo de metadados existe:
    metadata_file = os.path.join(folder_name, "metadata.json")
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"O arquivo de metadados {metadata_file} não existe.")

    try:
        # Carregar metadados:
        metadata = Metadata.load_from_json(metadata_file)

        # Verificar se a tabela existe:
        if table_name not in metadata.tables:
            raise ValueError(f"A tabela '{table_name}' não foi encontrada nos metadados")

        # Carregar dados reais e sintéticos para a tabela especificada:
        real_path = os.path.join(folder_name, f"{table_name}.csv")
        synthetic_path = os.path.join("synthetic_data", f"{table_name}.csv")

        # Verificar se os arquivos de dados reais e sintéticos existem:
        if not os.path.exists(real_path):
            raise FileNotFoundError(f"Arquivo de dados reais não encontrado: {real_path}")
        if not os.path.exists(synthetic_path):
            raise FileNotFoundError(f"Arquivo de dados sintéticos não encontrado: {synthetic_path}")

        real_data = pd.read_csv(real_path)
        synthetic_data = pd.read_csv(synthetic_path)

        # Verificar se a coluna existe:
        if column_name not in real_data.columns:
            raise ValueError(
                f"A coluna '{column_name}' não foi encontrada na tabela '{table_name}'"
            )

        # Criar dicionários de dados como exigido pelo get_column_plot:
        real_data_dict = {table_name: real_data}
        synthetic_data_dict = {table_name: synthetic_data}

        # Criar pasta de visualização se não existir:
        os.makedirs(visualization_folder, exist_ok=True)

        # Gerar plot de coluna:
        fig = get_column_plot(
            real_data=real_data_dict,
            synthetic_data=synthetic_data_dict,
            metadata=metadata,
            table_name=table_name,
            column_name=column_name,
        )

        if fig is None:
            raise ValueError(
                f"Não foi possível gerar visualização para {table_name}.{column_name}"
            )

        # Criar nome de arquivo:
        safe_column_name = column_name.replace(" ", "_").replace("/", "_")
        filename = f"{table_name}_{safe_column_name}.png"
        filepath = os.path.join(visualization_folder, filename)

        # Salvar a figura e retornar mensagem de sucesso:
        fig.write_image(filepath)
        return f"Visualização para {table_name}.{column_name} salva com sucesso em {os.path.abspath(filepath)}"
    
    # Tratamento de exceções durante a visualização:
    except Exception as e:
        raise RuntimeError(f"Ocorreu um erro durante a visualização: {e}")
    