from src.storage import init_db, last_two, save_record


def make_record():
    return {
        "city": "Москва",
        "time": "2026-07-28T12:00",
        "latitude": 55.75,
        "longitude": 37.62,
        "temperature": 21.3,
        "wind_speed": 3.5,
    }


def test_saved_record_can_be_read_back(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    record = make_record()

    save_record(record, db_path)
    result = last_two("Москва", db_path)

    assert len(result) == 1
    assert result[0] == record


def test_duplicate_city_time_is_ignored(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    record = make_record()

    save_record(record, db_path)
    save_record(record, db_path)

    assert len(last_two("Москва", db_path)) == 1
