import io

from src.report import (
    build_markdown,
    build_summary_markdown,
    compute_delta,
    print_report,
    write_report,
)


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


def _row_with_delta(delta):
    return {
        "city": "Москва",
        "temperature": 17.2,
        "temperature_delta": delta,
        "wind_speed": 2.6,
    }


def test_build_markdown_shows_zero_change_without_arrow():
    md = build_markdown([_row_with_delta(0.0)])

    assert md.splitlines()[-1] == "| Москва | 17.2 °C | 0.0 | 2.6 м/с |"


def test_build_markdown_treats_negative_zero_as_no_change():
    # compute_delta округляет -0.04 до -0.0 — стрелка вниз тут была бы ложью
    md = build_markdown([_row_with_delta(-0.0)])

    assert md.splitlines()[-1] == "| Москва | 17.2 °C | 0.0 | 2.6 м/с |"


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


def test_print_report_survives_non_utf8_console():
    # cp1251 не знает ↑ (U+2191): без перевода потока в UTF-8 вывод падал
    raw = io.BytesIO()
    stream = io.TextIOWrapper(raw, encoding="cp1251", newline="")
    md = build_markdown([_row_with_delta(1.5)])

    print_report(md, stream)
    stream.flush()

    assert raw.getvalue().decode("utf-8") == md + "\n"


def test_write_report_saves_utf8_regardless_of_locale(tmp_path):
    # читаем с явной UTF-8: тест не зависит от локали машины
    target = tmp_path / "report.md"
    md = build_markdown([_row_with_delta(1.5)])

    write_report(md, target)

    assert target.read_text(encoding="utf-8") == md + "\n"
    assert "↑" in target.read_bytes().decode("utf-8")
