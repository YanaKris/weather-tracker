from datetime import datetime
from pathlib import Path

from src.config import CITIES
from src.fetch import fetch_weather
from src.report import (
    REPORT_PATH,
    build_markdown,
    build_summary_markdown,
    compute_delta,
    print_report,
    write_report,
)
from src.storage import DB_PATH, init_db, last_two, save_record, summary_by_city


def collect_current_rows(
    cities: list[dict], db_path: str | Path = DB_PATH
) -> list[dict]:

    rows = []
    for city in cities:
        recent = last_two(city["name"], db_path)
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


def build_report(
    rows: list[dict], summary: list[dict], now: datetime | None = None
) -> str:

    if now is None:
        now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
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


def main(db_path: str | Path = DB_PATH, report_path: str | Path = REPORT_PATH) -> None:
    init_db(db_path)
    for city in CITIES:
        save_record(fetch_weather(city), db_path)

    rows = collect_current_rows(CITIES, db_path)
    summary = summary_by_city(db_path)
    report = build_report(rows, summary)

    print_report(report)
    write_report(report, report_path)


if __name__ == "__main__":
    main()
