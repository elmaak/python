
import sqlite3
import pandas as pd

from config.settings import DB_PATH


def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS air_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                city TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                pm25 REAL,
                pm10 REAL,
                no2 REAL,
                co REAL,
                so2 REAL,
                o3 REAL,
                european_aqi REAL,
                us_aqi REAL,
                UNIQUE(date, city)
            )
        """)

        conn.commit()


def save_data(df):

    if df.empty:
        return 0

    columns = [
        "Date", "City", "Latitude", "Longitude",
        "PM2.5", "PM10", "NO2", "CO",
        "SO2", "O3", "European AQI", "US AQI"
    ]

    data = df.reindex(columns=columns).copy()

    data.columns = [
        "date", "city", "latitude", "longitude",
        "pm25", "pm10", "no2", "co",
        "so2", "o3", "european_aqi", "us_aqi"
    ]

    data["date"] = pd.to_datetime(
        data["date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d %H:%M:%S")

    records = data.astype(object).where(
        pd.notna(data), None
    ).to_records(index=False).tolist()

    with get_connection() as conn:

        before = conn.total_changes

        conn.executemany("""
            INSERT OR IGNORE INTO air_quality (
                date, city, latitude, longitude,
                pm25, pm10, no2, co, so2, o3,
                european_aqi, us_aqi
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, records)

        inserted = conn.total_changes - before

        conn.commit()

    return inserted


def load_data(city=None):

    query = "SELECT * FROM air_quality"
    params = []

    if city:
        query += " WHERE city = ?"
        params.append(city)

    query += " ORDER BY date"

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn,
            params=params
        )

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df


def clear_database():

    with get_connection() as conn:
        conn.execute("DELETE FROM air_quality")
        conn.commit()
