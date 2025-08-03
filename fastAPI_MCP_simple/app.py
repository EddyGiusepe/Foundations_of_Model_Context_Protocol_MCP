#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Seguir os seguintes passos e ver os prints neste diretório
==========================================================
1. Em terminal execute o comando ---> uv run app.py
2. Em outro terminal execute o comando ---> npx @modelcontextprotocol/inspector

Links de estudo
---------------
* https://www.youtube.com/watch?v=-XNHX1eXEJA
* https://github.com/tadata-org/fastapi_mcp?tab=readme-ov-file
* https://modelcontextprotocol.io/legacy/tools/inspector
"""
from fastapi import FastAPI
import uvicorn
from fastapi_mcp import FastApiMCP

app = FastAPI()


@app.post("/add")
async def add(a: float, b: float):
    return a + b


mcp = FastApiMCP(app)
# mcp.mount_http()
mcp.mount()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
