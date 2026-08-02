from src.fetch import parse_current_weather


def test_parse_current_weather_extracts_fields():
    payload = {
        "latitude": 55.75,
        "longitude": 37.62,
        "current": {
            "time": "2026-07-28T12:00",
            "temperature_2m": 21.3,
            "wind_speed_10m": 3.5,
        },
    }

    record = parse_current_weather(payload)

    assert record == {
        "time": "2026-07-28T12:00",
        "latitude": 55.75,
        "longitude": 37.62,
        "temperature": 21.3,
        "wind_speed": 3.5,
    }
