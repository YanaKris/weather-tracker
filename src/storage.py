import sqlite3

DB_PATH = "data/weather.db"


def init_db(db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS observations (
                city TEXT,
                time TEXT,
                latitude REAL,
                longitude REAL,
                temperature REAL,
                wind_speed REAL,
                UNIQUE(city, time)
            )
            """
        )


def save_record(record: dict, db_path: str = DB_PATH) -> None:
    """Вставляет один замер; повтор той же пары city+time игнорируется."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO observations
                (city, time, latitude, longitude, temperature, wind_speed)
            VALUES (:city, :time, :latitude, :longitude, :temperature, :wind_speed)
            """,
            record,
        )


def last_two(city: str, db_path: str = DB_PATH) -> list[dict]:
    """Возвращает до двух последних по времени замеров города (новейший первым)."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT city, time, latitude, longitude, temperature, wind_speed
            FROM observations
            WHERE city = ?
            ORDER BY time DESC
            LIMIT 2
            """,
            (city,),
        ).fetchall()
    return [dict(row) for row in rows]


def summary_by_city(db_path: str = DB_PATH) -> list[dict]:
    """Сводная статистика температуры по каждому городу за всю историю."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT city,
                   COUNT(*) AS measurements,
                   ROUND(AVG(temperature), 1) AS avg_t,
                   MIN(temperature) AS min_t,
                   MAX(temperature) AS max_t
            FROM observations
            GROUP BY city
            ORDER BY avg_t DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]
