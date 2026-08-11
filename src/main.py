"""Точка входа: связывает Extract -> Load -> Report."""

from datetime import datetime

from src.config import CITIES
from src.fetch import fetch_weather
from src.report import (
    build_markdown,
    build_summary_markdown,
    compute_delta,
    print_report,
    write_report,
)
from src.storage import init_db, last_two, save_record, summary_by_city


def collect_current_rows(cities: list[dict]) -> list[dict]:
    """По каждому городу берёт свежий замер и изменение относительно прошлого."""
    rows = []
    for city in cities:
        recent = last_two(city["name"])
        if not recent:
            continue
        current = recent[0]
        delta = None
        if len(recent) == 2:
            delta = compute_delta(recent[1], current)["temperature_delta"]
        rows.append(
            {
                "city": current["city"],
                "temperature": current["temperature"],
                "temperature_delta": delta,
                "wind_speed": current["wind_speed"],
            }
        )
    return rows


def build_report(rows: list[dict], summary: list[dict]) -> str:
    """Склеивает полный отчёт: заголовок + таблица замеров + таблица сводки."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return "\n".join(
        [
            f"# Отчёт о погоде — {timestamp}",
            "",
            "## Текущие замеры",
            "",
            build_markdown(rows),
            "",
            "## Сводка за всё время наблюдений",
            "",
            build_summary_markdown(summary),
        ]
    )


def main() -> None:
    init_db()
    for city in CITIES:
        save_record(fetch_weather(city))

    rows = collect_current_rows(CITIES)
    summary = summary_by_city()
    report = build_report(rows, summary)

    print_report(report)
    write_report(report)


if __name__ == "__main__":
    main()
