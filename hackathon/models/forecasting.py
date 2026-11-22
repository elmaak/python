
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def create_features(series):

    data = pd.DataFrame({
        "target": series
    })

    for lag in [1, 2, 3, 7, 14, 24, 48]:

        data[f"lag_{lag}"] = (
            data["target"].shift(lag)
        )

    data["rolling_mean_24"] = (
        data["target"]
        .shift(1)
        .rolling(24)
        .mean()
    )

    data["rolling_std_24"] = (
        data["target"]
        .shift(1)
        .rolling(24)
        .std()
    )

    data["hour"] = data.index.hour
    data["day_of_week"] = data.index.dayofweek
    data["month"] = data.index.month

    return data.dropna()


def train_forecast_model(
    df,
    city,
    pollutant="PM2.5",
    forecast_hours=24
):

    city_data = df[
        df["City"] == city
    ].copy()

    series = (
        city_data.set_index("Date")[pollutant]
        .sort_index()
        .resample("h")
        .mean()
        .dropna()
    )

    if len(series) < 200:
        raise ValueError(
            "At least 200 hourly observations required."
        )

    dataset = create_features(series)

    if len(dataset) < 100:
        raise ValueError("Insufficient training data.")

    X = dataset.drop(columns="target")
    y = dataset["target"]

    split = int(len(dataset) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    model = RandomForestRegressor(
        n_estimators=250,
        max_depth=12,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(
            y_test, predictions
        ),
        "RMSE": np.sqrt(
            mean_squared_error(
                y_test, predictions
            )
        ),
        "R2": r2_score(
            y_test, predictions
        )
    }

    model.fit(X, y)

    history = series.copy()
    future_records = []

    for _ in range(forecast_hours):

        next_date = (
            history.index[-1]
            + pd.Timedelta(hours=1)
        )

        row = {
            "hour": next_date.hour,
            "day_of_week": next_date.dayofweek,
            "month": next_date.month
        }

        for lag in [1, 2, 3, 7, 14, 24, 48]:
            row[f"lag_{lag}"] = history.iloc[-lag]

        row["rolling_mean_24"] = (
            history.iloc[-24:].mean()
        )

        row["rolling_std_24"] = (
            history.iloc[-24:].std()
        )

        features = pd.DataFrame([row])

        prediction = max(
            0,
            float(model.predict(features)[0])
        )

        future_records.append({
            "Date": next_date,
            "Forecast": prediction
        })

        history.loc[next_date] = prediction

    return {
        "model": model,
        "metrics": metrics,
        "future": pd.DataFrame(future_records),
        "historical": series,
        "feature_importance": pd.DataFrame({
            "Feature": X.columns,
            "Importance": model.feature_importances_
        }).sort_values(
            "Importance",
            ascending=False
        )
    }
