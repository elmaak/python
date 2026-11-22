
import requests
import pandas as pd

from datetime import date, timedelta

from config.settings import (
    API_URL,
    API_VARIABLES,
    CITIES
)


def fetch_air_quality(
    city,
    start_date=None,
    end_date=None
):

    if city not in CITIES:
        raise ValueError("Unknown city.")

    location = CITIES[city]

    if start_date is None:
        start_date = date.today() - timedelta(days=7)

    if end_date is None:
        end_date = date.today()

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": ",".join(API_VARIABLES),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "timezone": location["timezone"]
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    payload = response.json()

    if "hourly" not in payload:
        raise ValueError("No hourly data returned.")

    hourly = payload["hourly"]

    df = pd.DataFrame(hourly)

    df["Date"] = pd.to_datetime(
        df.pop("time"),
        errors="coerce"
    )

    df["City"] = city

    df["Latitude"] = payload.get(
        "latitude",
        location["latitude"]
    )

    df["Longitude"] = payload.get(
        "longitude",
        location["longitude"]
    )

    rename = {
        "pm2_5": "PM2.5",
        "pm10": "PM10",
        "nitrogen_dioxide": "NO2",
        "carbon_monoxide": "CO",
        "sulphur_dioxide": "SO2",
        "ozone": "O3",
        "european_aqi": "European AQI",
        "us_aqi": "US AQI"
    }

    df = df.rename(columns=rename)

    return df


def fetch_multiple_cities(
    cities,
    start_date=None,
    end_date=None
):

    results = []

    for city in cities:

        try:

            result = fetch_air_quality(
                city,
                start_date,
                end_date
            )

            results.append(result)

        except (requests.RequestException, ValueError) as exc:

            print(f"Error for {city}: {exc}")

    if not results:
        return pd.DataFrame()

    return pd.concat(
        results,
        ignore_index=True
    )
