import json
import os
import copy
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any


SHIPMENTS_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "shipments.json")
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


def _load_shipments() -> Dict[str, Any]:
    with open(SHIPMENTS_DATA_PATH, "r") as f:
        return json.load(f)


def _save_shipments(data: Dict[str, Any]):
    with open(SHIPMENTS_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _simulate_position_update(shipment: Dict[str, Any], hours_passed: int = 6):
    dest_lat, dest_lon = 18.5204, 73.8567
    current_lat = shipment.get("position_lat", dest_lat)
    current_lon = shipment.get("position_lon", dest_lon)

    if shipment["status"] == "In Transit":
        progress = shipment.get("progress_pct", 0)
        progress_increment = min(5 * (hours_passed / 6), 100 - progress)
        shipment["progress_pct"] = min(100, progress + progress_increment)

        speed_factor = shipment["progress_pct"] / 100.0
        shipment["position_lat"] = current_lat + (dest_lat - current_lat) * 0.02
        shipment["position_lon"] = current_lon + (dest_lon - current_lon) * 0.02
        shipment["eta_days"] = max(1, int(shipment.get("eta_days", 5) - 0.25))

        if shipment["progress_pct"] >= 95:
            shipment["status"] = "Arrived"
            shipment["eta_days"] = 0

    elif shipment["status"] == "Customs Clearance":
        shipment["eta_days"] = max(1, shipment.get("eta_days", 8) - 0.25)
        if datetime.now().hour % 12 == 0:
            shipment["status"] = "In Transit"

    elif shipment["status"] == "Delayed":
        shipment["eta_days"] = shipment.get("eta_days", 12) - 0.25

    shipment["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


async def get_live_weather(lat: float = 18.5204, lon: float = 73.8567) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "wind_speed_10m", "precipitation", "weather_code"],
        "hourly": ["temperature_2m", "wind_speed_10m", "precipitation"],
        "timezone": "auto",
        "forecast_days": 7,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)
        data = response.json()

    wind_speed = data["current"]["wind_speed_10m"]
    precipitation = data["current"]["precipitation"]
    is_safe = wind_speed < 35 and (precipitation is None or precipitation < 5)

    return {
        "location": "Pune, India",
        "current": {
            "temperature": data["current"]["temperature_2m"],
            "wind_speed": wind_speed,
            "precipitation": precipitation,
            "weather_code": data["current"]["weather_code"],
        },
        "hourly": data["hourly"],
        "operation_safe": is_safe,
        "warning": None if is_safe else "High wind or precipitation - outdoor operations not safe!",
    }


def get_supply_chain_tracking() -> Dict[str, Any]:
    data = _load_shipments()
    for shipment in data["shipments"]:
        _simulate_position_update(shipment)
    _save_shipments(data)
    return data
