
import httpx
from typing import Dict, Any


WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


async def get_live_weather(lat: float = 18.5204, lon: float = 73.8567) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "wind_speed_10m", "precipitation", "weather_code"],
        "hourly": ["temperature_2m", "wind_speed_10m", "precipitation"],
        "timezone": "auto",
        "forecast_days": 7
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)
        data = response.json()

    wind_speed = data["current"]["wind_speed_10m"]
    precipitation = data["current"]["precipitation"]
    is_safe = wind_speed < 35 and precipitation < 5

    return {
        "location": "Pune, India",
        "current": {
            "temperature": data["current"]["temperature_2m"],
            "wind_speed": wind_speed,
            "precipitation": precipitation,
            "weather_code": data["current"]["weather_code"]
        },
        "hourly": data["hourly"],
        "operation_safe": is_safe,
        "warning": None if is_safe else "High wind or precipitation - outdoor operations not safe!"
    }


def get_supply_chain_tracking() -> Dict[str, Any]:
    return {
        "shipments": [
            {
                "id": "SHP-001",
                "item": "2MW Diesel Generator",
                "origin": "Chennai, India",
                "destination": "Pune, India",
                "status": "In Transit",
                "eta_days": 5,
                "route": "NH48",
                "mitigations": [
                    {
                        "option": "Air Freight Replacement",
                        "cost_usd": 18000,
                        "time_saved_days": 14
                    }
                ]
            },
            {
                "id": "SHP-002",
                "item": "UPS Modules (N+2)",
                "origin": "Singapore",
                "destination": "Pune, India",
                "status": "Customs Clearance",
                "eta_days": 8,
                "route": "Sea + Road",
                "mitigations": [
                    {
                        "option": "Expedite Customs",
                        "cost_usd": 2500,
                        "time_saved_days": 3
                    }
                ]
            }
        ]
    }

