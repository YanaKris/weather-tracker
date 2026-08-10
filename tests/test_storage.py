from src.storage import init_db, last_two, save_record, summary_by_city


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


def make_record_summary(time, temperature):
    return {
        "city": "Москва",
        "time": time,
        "latitude": 55.75,
        "longitude": 37.62,
        "temperature": temperature,
        "wind_speed": 3.5,
    }


def test_summary_by_city_computes_stats(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    record_1 = make_record_summary("2026-07-28T12:00", 20)
    record_2 = make_record_summary("2026-07-28T14:00", 30)
    record_3 = make_record_summary("2026-07-28T15:00", 10)
    save_record(record_1, db_path)
    save_record(record_2, db_path)
    save_record(record_3, db_path)
    result = summary_by_city(db_path)
    assert len(result) == 1
    assert result[0]["measurements"] == 3
    assert result[0]["avg_t"] == 20.0
    assert result[0]["min_t"] == 10.0
    assert result[0]["max_t"] == 30.0
