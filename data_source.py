import requests
from datetime import datetime, timezone
from config import OPENWEATHER_API_KEY

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


def get_coordinates(city_name: str):
    """Convert a city name into (lat, lon) using OpenWeatherMap Geocoding API."""
    params = {"q": city_name, "limit": 1, "appid": OPENWEATHER_API_KEY}
    response = requests.get(GEO_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"City '{city_name}' not found.")

    return data[0]["lat"], data[0]["lon"]


def get_current_reading(city_name: str) -> dict:
    """Fetch current air quality reading for a city. Returns a standardized dict."""
    lat, lon = get_coordinates(city_name)

    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY}
    response = requests.get(AIR_POLLUTION_URL, params=params)
    response.raise_for_status()
    data = response.json()["list"][0]

    components = data["components"]
    return {
        "city": city_name,
        "aqi": data["main"]["aqi"],  # 1 (Good) to 5 (Very Poor)
        "co": components.get("co"),
        "no2": components.get("no2"),
        "o3": components.get("o3"),
        "so2": components.get("so2"),
        "pm2_5": components.get("pm2_5"),
        "pm10": components.get("pm10"),
        "nh3": components.get("nh3"),
        "timestamp": datetime.fromtimestamp(data["dt"], tz=timezone.utc).isoformat(),
    }


# Quick manual test
if __name__ == "__main__":
    city = "Lahore"
    reading = get_current_reading(city)
    for key, value in reading.items():
        print(f"{key}: {value}")