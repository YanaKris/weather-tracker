"""Transform: расчёт изменений и сборка Markdown-отчёта."""


def compute_delta(previous: dict, current: dict) -> dict:
    """Возвращает изменение температуры и ветра между двумя замерами."""
    temp = current["temperature"] - previous["temperature"]
    wind = current["wind_speed"] - previous["wind_speed"]
    return {
        "temperature_delta": round(temp, 1),
        "wind_speed_delta": round(wind, 1),
    }


def _format_change(delta: float | None) -> str:
    """Готовит текст для колонки «Изменение»: со знаком и стрелкой или «—»."""
    if delta is None:
        return "—"
    if delta > 0:
        return f"+{delta} ↑"
    if delta < 0:
        return f"{delta} ↓"
    return "0.0"


def build_markdown(rows: list[dict]) -> str:
    """Собирает Markdown-таблицу текущих замеров по городам."""
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
    """Собирает Markdown-таблицу сводной статистики по городам."""
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
