# <h1 align="center"><font color="gree">MCP Greeter</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

## <font color="blue">Sobre o Projeto</font>
Este é um exemplo simples de implementação do Model Context Protocol (MCP) que consiste em um servidor e cliente para troca de mensagens de saudação.

## <font color="blue">Estrutura do Projeto</font>
- `greeter.py`: Servidor MCP que fornece uma ferramenta de saudação
- `client_greeter.py`: Cliente que se conecta ao servidor e processa saudações

## <font color="blue">Componentes</font>

### <font color="red">Servidor MCP (greeter.py)</font>
O servidor implementa uma ferramenta simples chamada `greet` que retorna uma mensagem de boas-vindas.

```python
@mcp.tool()
def greet() -> str:
    """Retorna esta mensagem de boas-vindas, quando cumprimentado com "Olá", "Oi" ou "Hey"."""
    return "Olá Eddy Giusepe, Bem-vindo ao mundo dos MCPs!"
```

### <font color="red">Cliente MCP (client_greeter.py)</font>
O cliente se conecta ao servidor MCP e fornece uma interface interativa para enviar saudações.

## <font color="blue">Como Executar</font>

1. Instale as dependências necessárias:
```bash
uv add mcp anthropic python-dotenv
```

2. Execute o cliente, passando o caminho para o servidor:
```bash
uv run client_greeter.py /caminho/para/greeter.py
```

3. No prompt interativo, digite uma das saudações aceitas:
   - "Olá"
   - "Oi"
   - "Hey"

4. Para sair do programa, digite "quit".

## <font color="blue">Fluxo de Funcionamento</font>
1. O cliente inicia e se conecta ao servidor MCP
2. O servidor disponibiliza a ferramenta "greet"
3. O usuário envia uma saudação através do cliente
4. O cliente processa a saudação e chama a ferramenta apropriada
5. O servidor responde com uma mensagem de boas-vindas
6. O cliente exibe a resposta ao usuário




Thank God!