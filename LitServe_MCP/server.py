#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Run
===
uv run server.py
"""
from transformers import pipeline
from pydantic import BaseModel
from litserve.mcp import MCP
import litserve as ls

class TextClassificationRequest(BaseModel):
    input: str

class TextClassificationAPI(ls.LitAPI):
    def setup(self, device):
        self.model = pipeline("sentiment-analysis", model="lucas-leme/FinBERT-PT-BR", device=device)

    def decode_request(self, request: TextClassificationRequest):
        return request.input

    def predict(self, x):
        return self.model(x)
    
    def encode_response(self, output):
        return output[0]

if __name__ == "__main__":
    api = TextClassificationAPI(mcp=MCP(description="Classifica sentimentos em textos"))
    server = ls.LitServer(api)
    server.run(port=8000)
