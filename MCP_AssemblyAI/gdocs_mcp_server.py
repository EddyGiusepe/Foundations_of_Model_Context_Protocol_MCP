#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
from typing import Any
from mcp.server.fastmcp import FastMCP
from doc_tools import create_document

mcp = FastMCP("google_docs")

def format_response(response: str) -> str:
    return f"Response: {response}"

@mcp.tool()
async def create_google_doc(title: str, text: str) -> str:
    result = create_document(title, text)
    return format_response(result)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
