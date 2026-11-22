
import pandas as pd
import numpy as np


POLLUTANT_COLUMNS = [
    "PM2.5",
    "PM10",
    "NO2",
    "CO",
    "SO2",
    "O3",
    "European AQI",
    "US AQI"
]


def clean_data(df):

    if df.empty:
        return df.copy(), {}

    data = df.copy()

    original_rows = len(data)

    data.columns = data.columns.str.strip()

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Date", "City"]
    )

    duplicates = int(
        data.duplicated(
            subset=["Date", "City"]
        ).sum()
    )

    data = data.drop_duplicates(
        subset=["Date", "City"],
        keep="last"
    )

    available = [
        col for col in POLLUTANT_COLUMNS
        if col in data.columns
    ]

    for col in available:

        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )

        data.loc[data[col] < 0, col] = np.nan

    missing_before = data[available].isna().sum()

    data = data.sort_values(
        ["City", "Date"]
    )

    for col in available:

        data[col] = (
            data.groupby("City")[col]
            .transform(
                lambda x: x.interpolate(
                    method="linear",
                    limit=3,
                    limit_area="inside"
                )
            )
        )

    report = {
        "original_rows": original_rows,
        "cleaned_rows": len(data),
        "removed_rows": original_rows - len(data),
        "duplicates_removed": duplicates,
        "missing_before": missing_before.to_dict(),
        "missing_after": data[available].isna().sum().to_dict(),
        "missing_total_after": int(
            data[available].isna().sum().sum()
        )
    }

    return data.reset_index(drop=True), report


def detect_iqr_outliers(df, column):

    values = df[column].dropna()

    if len(values) < 4:
        return pd.Series(False, index=df.index)

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return (
        (df[column] < lower)
        | (df[column] > upper)
    ).fillna(False)
