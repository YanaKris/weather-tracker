from src.report import build_markdown, build_summary_markdown, compute_delta


def test_compute_delta_returns_signed_changes():
    previous = {"temperature": 20.0, "wind_speed": 3.0}
    current = {"temperature": 21.5, "wind_speed": 2.5}

    result = compute_delta(previous, current)

    assert result == {"temperature_delta": 1.5, "wind_speed_delta": -0.5}


def test_build_markdown_renders_table():
    rows = [
        {
            "city": "Москва",
            "temperature": 17.2,
            "temperature_delta": 1.5,
            "wind_speed": 2.6,
        },
        {
            "city": "Санкт-Петербург",
            "temperature": 15.0,
            "temperature_delta": -0.4,
            "wind_speed": 5.1,
        },
        {
            "city": "Новосибирск",
            "temperature": 24.7,
            "temperature_delta": None,
            "wind_speed": 2.0,
        },
    ]

    md = build_markdown(rows)

    assert md == (
        "| Город | Температура | Изменение | Ветер |\n"
        "| --- | --- | --- | --- |\n"
        "| Москва | 17.2 °C | +1.5 ↑ | 2.6 м/с |\n"
        "| Санкт-Петербург | 15.0 °C | -0.4 ↓ | 5.1 м/с |\n"
        "| Новосибирск | 24.7 °C | — | 2.0 м/с |"
    )


def test_build_summary_markdown_renders_table():
    summary = [
        {
            "city": "Москва",
            "measurements": 3,
            "avg_t": 20.0,
            "min_t": 10.0,
            "max_t": 30.0,
        },
        {
            "city": "Новосибирск",
            "measurements": 2,
            "avg_t": 15.0,
            "min_t": 12.0,
            "max_t": 18.0,
        },
    ]

    md = build_summary_markdown(summary)

    assert md == (
        "| Город | Замеров | Средняя | Минимум | Максимум |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Москва | 3 | 20.0 °C | 10.0 °C | 30.0 °C |\n"
        "| Новосибирск | 2 | 15.0 °C | 12.0 °C | 18.0 °C |"
    )
