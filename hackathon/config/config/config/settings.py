
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

DB_PATH = DATABASE_DIR / "airvision.db"

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

DEFAULT_CITY = "Prishtina"

CITIES = {
    "Prishtina": {
        "latitude": 42.6629,
        "longitude": 21.1655,
        "timezone": "Europe/Belgrade"
    },
    "Tirana": {
        "latitude": 41.3275,
        "longitude": 19.8187,
        "timezone": "Europe/Tirane"
    },
    "Skopje": {
        "latitude": 41.9981,
        "longitude": 21.4254,
        "timezone": "Europe/Skopje"
    },
    "Sarajevo": {
        "latitude": 43.8563,
        "longitude": 18.4131,
        "timezone": "Europe/Sarajevo"
    },
    "Berlin": {
        "latitude": 52.5200,
        "longitude": 13.4050,
        "timezone": "Europe/Berlin"
    },
    "Vienna": {
        "latitude": 48.2082,
        "longitude": 16.3738,
        "timezone": "Europe/Vienna"
    }
}

API_VARIABLES = [
    "pm2_5",
    "pm10",
    "nitrogen_dioxide",
    "carbon_monoxide",
    "sulphur_dioxide",
    "ozone",
    "european_aqi",
    "us_aqi"
]

POLLUTANT_LABELS = {
    "pm2_5": "PM2.5",
    "pm10": "PM10",
    "nitrogen_dioxide": "NO2",
    "carbon_monoxide": "CO",
    "sulphur_dioxide": "SO2",
    "ozone": "O3",
    "european_aqi": "European AQI",
    "us_aqi": "US AQI"
}

POLLUTANTS = list(POLLUTANT_LABELS.values())

for folder in [DATA_DIR, DATABASE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)
