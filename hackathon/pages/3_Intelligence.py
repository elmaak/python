
import streamlit as st

from sklearn.ensemble import IsolationForest

from models.forecasting import train_forecast_model

from components.charts import (
    anomaly_chart,
    forecast_chart
)


st.set_page_config(
    page_title="AI Intelligence | AIRVISION",
    layout="wide"
)

st.title("🤖 AI Intelligence Center")

if "active_data" not in st.session_state:
    st.warning("Load data from dashboard first.")
    st.stop()

df = st.session_state["active_data"].copy()

city = st.selectbox(
    "Select city",
    sorted(df["City"].unique())
)

pollutant = st.selectbox(
    "Select pollutant",
    ["PM2.5", "PM10", "NO2", "CO"]
)

city_data = df[
    df["City"] == city
].sort_values("Date").copy()

tab1, tab2 = st.tabs([
    "Anomaly Detection",
    "Forecasting"
])

with tab1:

    contamination = st.slider(
        "Anomaly proportion",
        0.01, 0.15, 0.03
    )

    if st.button("Run Anomaly Detection"):

        values = city_data[
            [pollutant]
        ].dropna()

        if len(values) < 30:

            st.warning("Not enough observations.")

        else:

            model = IsolationForest(
                n_estimators=200,
                contamination=contamination,
                random_state=42
            )

            result = city_data.loc[
                values.index
            ].copy()

            result["Prediction"] = (
                model.fit_predict(values)
            )

            result["Status"] = (
                result["Prediction"].map({
                    1: "Normal",
                    -1: "Anomaly"
                })
            )

            st.session_state["anomaly_results"] = result

    if "anomaly_results" in st.session_state:

        result = st.session_state["anomaly_results"]

        st.plotly_chart(
            anomaly_chart(result, pollutant),
            use_container_width=True
        )

        anomalies = result[
            result["Status"] == "Anomaly"
        ]

        st.metric(
            "Detected anomalies",
            len(anomalies)
        )

        st.dataframe(anomalies)

with tab2:

    horizon = st.slider(
        "Forecast hours",
        6, 72, 24, step=6
    )

    if st.button("Train Random Forest"):

        try:

            with st.spinner("Training model..."):

                result = train_forecast_model(
                    df,
                    city,
                    pollutant,
                    horizon
                )

                st.session_state["forecast_results"] = result

        except Exception as exc:

            st.error(str(exc))

    if "forecast_results" in st.session_state:

        result = st.session_state["forecast_results"]

        metrics = result["metrics"]

        c1, c2, c3 = st.columns(3)

        c1.metric("MAE", f"{metrics['MAE']:.3f}")
        c2.metric("RMSE", f"{metrics['RMSE']:.3f}")
        c3.metric("R²", f"{metrics['R2']:.3f}")

        st.plotly_chart(
            forecast_chart(
                result["historical"],
                result["future"],
                pollutant
            ),
            use_container_width=True
        )

        st.subheader("Feature Importance")

        st.dataframe(
            result["feature_importance"]
        )

        st.subheader("Predictions")

        st.dataframe(
            result["future"]
        )

