import subprocess
from pathlib import Path

import pytest

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
