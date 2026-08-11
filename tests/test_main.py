from datetime import datetime

from src.main import build_report, collect_current_rows
from src.storage import init_db, save_record

MOSCOW = {"name": "Москва", "latitude": 55.75, "longitude": 37.62}


def make_record(time, temperature, city="Москва", wind_speed=3.5):
    return {
        "city": city,
        "time": time,
        "latitude": 55.75,
        "longitude": 37.62,
        "temperature": temperature,
        "wind_speed": wind_speed,
    }


def test_collect_current_rows_computes_delta_from_previous_measurement(tmp_path):
    """Два замера в разные моменты — «Изменение» показывает разницу между ними."""
    db_path = tmp_path / "test.db"
    init_db(db_path)
    save_record(make_record("2026-08-11T13:00", 20.0), db_path)
    save_record(make_record("2026-08-11T14:00", 21.5), db_path)

    rows = collect_current_rows([MOSCOW], db_path)

    assert rows == [
        {
            "city": "Москва",
            "temperature": 21.5,
            "temperature_delta": 1.5,
            "wind_speed": 3.5,
        }
    ]


def test_collect_current_rows_has_no_delta_on_first_measurement(tmp_path):
    """Первый замер сравнивать не с чем — дельта пустая, город в отчёте остаётся."""
    db_path = tmp_path / "test.db"
    init_db(db_path)
    save_record(make_record("2026-08-11T13:00", 20.0), db_path)

    rows = collect_current_rows([MOSCOW], db_path)

    assert len(rows) == 1
    assert rows[0]["temperature_delta"] is None


def test_collect_current_rows_skips_city_without_measurements(tmp_path):
    """Города без замеров в таблицу не попадают."""
    db_path = tmp_path / "test.db"
    init_db(db_path)

    assert collect_current_rows([MOSCOW], db_path) == []


def test_build_report_uses_injected_time():
    """Время отчёта инжектируется: иначе документ нельзя проверить тестом."""
    report = build_report([], [], now=datetime(2026, 8, 11, 15, 30))

    assert report.startswith("# Отчёт о погоде — 2026-08-11 15:30\n")


def test_build_report_contains_both_sections_with_tables():
    rows = [
        {
            "city": "Москва",
            "temperature": 21.5,
            "temperature_delta": 1.5,
            "wind_speed": 3.5,
        }
    ]
    summary = [
        {
            "city": "Москва",
            "measurements": 2,
            "avg_t": 20.8,
            "min_t": 20.0,
            "max_t": 21.5,
        }
    ]

    report = build_report(rows, summary, now=datetime(2026, 8, 11, 15, 30))

    assert "## Текущие замеры" in report
    assert "| Москва | 21.5 °C | +1.5 ↑ | 3.5 м/с |" in report
    assert "## Сводка за всё время наблюдений" in report
    assert "| Москва | 2 | 20.8 °C | 20.0 °C | 21.5 °C |" in report
