#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script poke.py
==============
Você pode usar o modo desenvolvimento, para testar a ferramenta.
No README mostrarei os detalhes.
mcp dev poke.py
"""
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("poke")

POKEAPI_BASE = "https://pokeapi.co/api/v2"  # https://pokeapi.co/


# --- Auxiliar para buscar dados de Pokémon ---
async def fetch_pokemon_data(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{POKEAPI_BASE}/pokemon/{name.lower()}")
            if response.status_code == 200:
                return response.json()
        except httpx.HTTPError:
            pass
    return {}


# --- Ferramenta (Tool): Obter informações sobre um Pokémon ---
@mcp.tool()
async def get_pokemon_info(name: str) -> str:
    """Obter informações detalhadas sobre um Pokémon pelo nome."""
    data = await fetch_pokemon_data(name)
    if not data:
        return f"No data found for Pokémon: {name}"

    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
    types_ = [t["type"]["name"] for t in data["types"]]
    abilities = [a["ability"]["name"] for a in data["abilities"]]

    return f"""
Name: {data['name'].capitalize()}
Types: {', '.join(types_)}
Abilities: {', '.join(abilities)}
Stats: {', '.join(f"{k}: {v}" for k, v in stats.items())}
"""


# --- Ferramenta (Tool): Criar um time de Pokémon para um torneio ---
@mcp.tool()
async def create_tournament_squad() -> str:
    """Criar um time poderoso de Pokémon para um torneio."""
    top_pokemon = [
        "charizard",
        "garchomp",
        "lucario",
        "dragonite",
        "metagross",
        "gardevoir",
    ]
    squad = []

    for name in top_pokemon:
        data = await fetch_pokemon_data(name)
        if data:
            squad.append(data["name"].capitalize())

    return "Tournament Squad:\n" + "\n".join(squad)


# --- Ferramenta (Tool): Listar Pokémon populares ---
@mcp.tool()
async def list_popular_pokemon() -> str:
    """Listar Pokémon populares para torneios."""
    return "\n".join(
        ["Charizard", "Garchomp", "Lucario", "Dragonite", "Metagross", "Gardevoir"]
    )


# --- Ponto de entrada ---
if __name__ == "__main__":
    mcp.run(transport="stdio")
