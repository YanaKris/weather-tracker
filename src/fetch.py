import requests

API_URL = "https://api.open-meteo.com/v1/forecast"


def parse_current_weather(payload: dict) -> dict:

    current = payload["current"]
    return {
        "time": current["time"],
        "latitude": payload["latitude"],
        "longitude": payload["longitude"],
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
    }


def fetch_weather(city: dict) -> dict:

    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "temperature_2m,wind_speed_10m",
        "wind_speed_unit": "ms",
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    record = parse_current_weather(response.json())
    record["city"] = city["name"]
    return record


if __name__ == "__main__":
    moscow = {"name": "Москва", "latitude": 55.75, "longitude": 37.62}
    print(fetch_weather(moscow))
