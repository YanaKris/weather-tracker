"""Пути проекта: якорь на корень репозитория, а не на CWD процесса.

Относительные пути ломались при запуске из любого каталога, кроме корня:
база падала с OperationalError, а отчёт молча уезжал в чужой каталог.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
