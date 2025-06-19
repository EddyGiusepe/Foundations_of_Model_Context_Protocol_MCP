#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Inicia servidor FastMCP:
mcp = FastMCP("weather")

# Constantes:
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Faz uma solicitação à API NWS com tratamento de erros apropriado."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Formata uma característica de alerta em uma string legível."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Obtém alertas meteorológicos para um estado dos EUA.

    Args:
        state: Código de estado dos EUA de dois dígitos (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Não foi possível buscar alertas ou nenhum alerta encontrado."

    if not data["features"]:
        return "Nenhum alerta ativo para este estado."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Obtém previsão do tempo para uma localização.

    Args:
        latitude: Latitude da localização
        longitude: Longitude da localização
    """
    # Primeiro, obtenha o endpoint de grade de previsão
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Obtenha o URL da previsão da resposta de pontos
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Não foi possível buscar previsão detalhada."

    # Formata os períodos em uma previsão legível
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Apenas mostrar os próximos 5 períodos
        forecast = f"""
{period['name']}:
Temperatura: {period['temperature']}°{period['temperatureUnit']}
Vento: {period['windSpeed']} {period['windDirection']}
Previsão: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    # Inicia e executa o servidor
    mcp.run(transport="stdio")
