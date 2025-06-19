# <h1 align="center"><font color="gree">MCP FileCounter</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

## <font color="blue">Sobre o Projeto</font>
Este projeto implementa um sistema baseado no Model Context Protocol (MCP) que conta arquivos em diretórios especificados pelo usuário. O diferencial é a integração com a `API do Anthropic Claude`, permitindo que o usuário faça perguntas em linguagem natural sobre a quantidade de arquivos em diretórios.

## <font color="blue">Estrutura do Projeto</font>
- `filecounter.py`: Servidor MCP que fornece a ferramenta de contagem de arquivos
- `client_filecounter.py`: Cliente que se conecta ao servidor e processa comandos do usuário usando `IA`

## <font color="blue">Componentes</font>

### <font color="red">Servidor MCP (filecounter.py)</font>
O servidor implementa uma ferramenta (`Tool`) chamada `count_files` que conta o número de arquivos em um diretório especificado.

```python
@mcp.tool()
def count_files(directory_path: str = "/home/karinag/Documentos") -> str:
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
```

### <font color="red">Cliente MCP com IA (client_filecounter.py)</font>

O cliente se conecta ao servidor MCP e fornece uma interface interativa que usa o modelo `Claude` para:
1. Interpretar comandos em linguagem natural
2. Extrair caminhos de diretório das perguntas do usuário
3. Formatar respostas de maneira natural e clara

## <font color="blue">Como Executar</font>

1. Instale as dependências necessárias:
```bash
uv add mcp anthropic python-dotenv
```

2. Configure sua chave API do Anthropic no arquivo config/settings.py:
```python
ANTHROPIC_API_KEY = "sua_chave_api_aqui"
```

3. Execute o cliente, passando o caminho para o servidor:
```bash
uv run client_filecounter.py /caminho/para/filecounter.py
```

4. No prompt interativo, faça perguntas em linguagem natural como:
   - "Quantos arquivos tem na pasta `/home/karinag/Documentos`?"
   - "Contar arquivos em `/home/karinag/Image`"
   - "Analise os arquivos da pasta `/home/karinag`"

5. Para sair do programa, digite `"quit"`.

## <font color="blue">Fluxo de Funcionamento</font>

1. O cliente inicia e se conecta ao servidor MCP
2. O servidor disponibiliza a ferramenta (Tool) "count_files"
3. O usuário envia uma pergunta em linguagem natural
4. O cliente usa a `API do Claude` para interpretar a pergunta e extrair o caminho do diretório
5. O cliente chama a ferramenta `"count_files"` com o caminho extraído
6. O servidor conta os arquivos e retorna o resultado
7. O cliente usa novamente a `API do Claude` para formatar uma resposta natural
8. O cliente exibe a resposta formatada ao usuário

## <font color="blue">Benefícios da Integração com `IA`</font>

- Interface mais natural e amigável para o usuário
- Capacidade de interpretar comandos variados sem sintaxe rígida
- Respostas contextualizadas e em linguagem natural
- Demonstração prática de como integrar LLMs com ferramentas MCP






Thank God!