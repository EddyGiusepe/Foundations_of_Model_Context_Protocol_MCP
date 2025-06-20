# <h1 align="center"><font color="gree">Pokemon MCP Server</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Link de estudo: [mcp pokemon](https://www.youtube.com/watch?v=Fhy_VFMlE9s)


## Instalação e Configuração

Para executar este servidor Pokemon MCP, siga os passos abaixo:

### 1. Instalação do Node.js

Remova versões anteriores ou pacotes conflitantes:
```bash
sudo apt purge nodejs npm libnode-dev libnode72
sudo apt autoremove
sudo apt clean
```

Adicione o repositório NodeSource para a versão 18:
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
```

Instale o Node.js:
```bash
sudo apt install -y nodejs
```

Se encontrar erros de conflito de pacotes, use:
```bash
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nodejs_*_amd64.deb
sudo apt --fix-broken install
```

Verifique a instalação:
```bash
node -v
npm -v
```

### 2. Instalação do MCP

Instale o pacote MCP:
```bash
pip install -U mcp
```

### 3. Executando o Servidor

Para iniciar o servidor e a interface web:
```bash
mcp dev poke.py
```

Acesse a interface no navegador através do endereço mostrado no terminal (geralmente http://localhost:8000).