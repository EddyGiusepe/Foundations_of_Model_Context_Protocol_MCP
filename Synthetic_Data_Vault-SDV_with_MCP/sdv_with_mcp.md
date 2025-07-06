# <h1 align="center"><font color="gree">Gerador de Dados Sintéticos alimentado por MCP</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Este tutorial está baseado no [Daily Dose of Data Science]()

![](https://www.dailydoseofds.com/content/images/2024/08/banner-mail.png)

![](https://www.bigdatawire.com/wp-content/uploads/2023/11/SDV_logo.png)


Aqui vamos a construir um servidor `MCP` que todo cientista de dados adoraria ter. É um servidor `MCP que pode gerar qualquer tipo de conjunto de dados sintéticos. Conjuntos de dados sintéticos são importantes porque nos fornecem mais dados de amostras existentes, especialmente quando os dados do mundo real são limitados, desequilibrados ou sensíveis.

Aqui está nossa pilha de tecnologia:

- `Cursor` como host MCP.
- [SDV](https://docs.sdv.dev/sdv?ref=dailydoseofds.com) ​para gerar dados sintéticos tabulares realistas.

[SDV é uma biblioteca Python](https://pypi.org/project/sdv/) que usa ML para criar dados sintéticos que se assemelham a padrões do mundo real. O processo envolve treinar um modelo, amostrar dados e validar com base no original.


![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1d7f775-6a62-4519-814c-b79fdedc177b_1280x668.gif)



A seguir se mostra uma visão geral do sistema que vamos construir:

![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45254dff-1dd3-4f53-99c4-e56e91663459_1280x1064.gif)


Basicamente, temos o seguinte processo:

* O usuário envia uma consulta
* O agente se conecta ao servidor `MCP` para encontrar ferramentas (tools)
* O agente utiliza a ferramenta apropriada com base na consulta
* Retorna resposta sobre criação, avaliação ou visualização de dados sintéticos












Thank God 🤓!

