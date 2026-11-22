
import pandas as pd


def calculate_kpis(df):

    if df.empty:
        return {}

    return {
        "records": len(df),
        "cities": df["City"].nunique(),
        "average_pm25": df["PM2.5"].mean(),
        "average_pm10": df["PM10"].mean(),
        "average_aqi": df["European AQI"].mean(),
        "maximum_pm25": df["PM2.5"].max()
    }


def aggregate_data(
    df,
    frequency="D",
    pollutant="PM2.5"
):

    return (
        df.set_index("Date")
        .groupby("City")[pollutant]
        .resample(frequency)
        .mean()
        .reset_index()
        .dropna(subset=[pollutant])
    )


def calculate_correlation(df):

    columns = [
        col for col in [
            "PM2.5", "PM10", "NO2",
            "CO", "SO2", "O3"
        ]
        if col in df.columns
    ]

    return df[columns].corr()


def calculate_moving_average(
    df,
    pollutant="PM2.5",
    window=24
):

    data = df.sort_values("Date").copy()

    data["Moving Average"] = (
        data.groupby("City")[pollutant]
        .transform(
            lambda x: x.rolling(
                window=window,
                min_periods=1
            ).mean()
        )
    )

    return data


def calculate_daily_statistics(df):

    return (
        df.groupby([
            "City",
            pd.Grouper(key="Date", freq="D")
        ])
        [["PM2.5", "PM10", "NO2", "CO"]]
        .agg(["mean", "max", "min", "std"])
        .reset_index()
    )


def get_pollution_category(aqi):

    if pd.isna(aqi):
        return "Unavailable"

    if aqi <= 20:
        return "Good"

    if aqi <= 40:
        return "Fair"

    if aqi <= 60:
        return "Moderate"

    if aqi <= 80:
        return "Poor"

    if aqi <= 100:
        return "Very Poor"

    return "Extremely Poor"
