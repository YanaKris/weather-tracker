import sys
from pathlib import Path
from typing import TextIO

from src.paths import PROJECT_ROOT

REPORT_PATH = PROJECT_ROOT / "report.md"


def compute_delta(previous: dict, current: dict) -> dict:

    temp = current["temperature"] - previous["temperature"]
    wind = current["wind_speed"] - previous["wind_speed"]
    return {
        "temperature_delta": round(temp, 1),
        "wind_speed_delta": round(wind, 1),
    }


def _format_change(delta: float | None) -> str:

    if delta is None:
        return "—"
    if delta > 0:
        return f"+{delta} ↑"
    if delta < 0:
        return f"{delta} ↓"
    return "0.0"


def build_markdown(rows: list[dict]) -> str:

    lines = [
        "| Город | Температура | Изменение | Ветер |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['city']} | {row['temperature']} °C "
            f"| {_format_change(row['temperature_delta'])} "
            f"| {row['wind_speed']} м/с |"
        )
    return "\n".join(lines)


def build_summary_markdown(summary: list[dict]) -> str:

    lines = [
        "| Город | Замеров | Средняя | Минимум | Максимум |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in summary:
        lines.append(
            f"| {row['city']} | {row['measurements']} "
            f"| {row['avg_t']} °C | {row['min_t']} °C | {row['max_t']} °C |"
        )
    return "\n".join(lines)


def write_report(markdown: str, path: str | Path = REPORT_PATH) -> None:

    Path(path).write_text(markdown + "\n", encoding="utf-8", newline="\n")


def print_report(markdown: str, stream: TextIO | None = None) -> None:
    """Печатает отчёт, переведя поток в UTF-8: на cp1251 стрелки роняют вывод."""
    stream = sys.stdout if stream is None else stream
    reconfigure = getattr(stream, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
    stream.write(markdown + "\n")
