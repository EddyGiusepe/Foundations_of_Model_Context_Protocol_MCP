# <h1 align="center"><font color="gree">Simple MCP Weather Server</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>


O `MCP` (Model Context Protocol) é um protocolo que permite conectar `servidores` a `clientes de IA`, como o Claude Desktop, expandindo as capacidades dos modelos de linguagem.

## <font color="blue">Principais conceitos do MCP</font>

O `MCP` permite que servidores forneçam três tipos principais de capacidades:

1. `Resources` (Recursos): Dados similares a arquivos que podem ser lidos pelos clientes (como respostas de API ou conteúdo de arquivos)

2. `Tools` (Ferramentas): Funções que podem ser chamadas pelo LLM (com aprovação do usuário)

3. `Prompts`: Templates pré-escritos que ajudam os usuários a realizar tarefas específicas

## <font color="blue">Como funciona</font>

Quando você faz uma pergunta:

- O cliente envia sua pergunta para o Claude
- O Claude analisa as ferramentas disponíveis e decide qual(is) usar
- O cliente executa a(s) ferramenta(s) escolhida(s) através do servidor `MCP`
- Os resultados são enviados de volta para o Claude
- O Claude formula uma resposta em linguagem natural
- A resposta é exibida para você

## <font color="blue">Exemplo prático</font>

Este tutorial mostra a construção de um `servidor de clima` que expõe duas ferramentas:

- `get-alerts`: Para obter alertas meteorológicos
- `get-forecast`: Para obter previsões do tempo

Isso resolve uma limitação comum dos `LLMs` que normalmente não conseguem buscar dados meteorológicos atualizados.

O `MCP` é especialmente útil para integrar `LLMs` com `APIs externas`, `bancos de dados` e outras fontes de dados em tempo real, expandindo significativamente suas capacidades além do conhecimento de treinamento.

