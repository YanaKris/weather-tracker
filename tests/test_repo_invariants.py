"""Инварианты репозитория, от которых зависит работа пайплайна (см. PLAN.md)."""

import subprocess
from pathlib import Path

import pytest

from src.report import REPORT_PATH
from src.storage import DB_PATH

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_weather_db_is_not_gitignored():
    """PLAN.md: база коммитится между запусками, иначе история обнуляется."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", "data/weather.db"],
        cwd=REPO_ROOT,
        capture_output=True,
    )

    if result.returncode == 128:
        pytest.skip("git недоступен или каталог не является git-репозиторием")
    assert result.returncode == 1, (
        "data/weather.db попал под .gitignore — при запуске по расписанию "
        "история наблюдений обнулится, и «Изменение» всегда покажет «—»"
    )


def test_weather_db_is_marked_binary():
    """Проверяем эффекты, а не написание макроса: важны сами три атрибута.

    Без -text база коммитится как текст, и core.autocrlf=true портит её
    заменой LF на CRLF внутри бинарного файла.
    """
    result = subprocess.run(
        ["git", "check-attr", "text", "diff", "merge", "--", "data/weather.db"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        pytest.skip("git недоступен или каталог не является git-репозиторием")
    attrs = result.stdout
    assert "text: unset" in attrs, (
        "data/weather.db не помечен бинарником: core.autocrlf=true испортит "
        f"базу переводом строк. Атрибуты сейчас:\n{attrs}"
    )
    assert "diff: unset" in attrs, f"git попытается показать базу текстом:\n{attrs}"
    assert "merge: unset" in attrs, (
        "git попытается слить базу как текст и допишет в неё маркеры "
        f"конфликта:\n{attrs}"
    )


def test_report_md_keeps_lf():
    """Отчёт пишется с LF намеренно (newline="\\n"), autocrlf не должен его менять."""
    result = subprocess.run(
        ["git", "check-attr", "eol", "--", "report.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        pytest.skip("git недоступен или каталог не является git-репозиторием")
    assert "eol: lf" in result.stdout, (
        "report.md не закреплён на LF: core.autocrlf=true заменит переводы строк "
        f"на CRLF при checkout. Атрибуты сейчас:\n{result.stdout}"
    )


def test_pipeline_paths_are_anchored_to_repo_root():
    """Пути не зависят от CWD: иначе запуск из другого каталога пишет не туда."""
    assert Path(DB_PATH) == REPO_ROOT / "data" / "weather.db"
    assert Path(REPORT_PATH) == REPO_ROOT / "report.md"
