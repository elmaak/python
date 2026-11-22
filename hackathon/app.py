
import streamlit as st
import pandas as pd

from datetime import date, timedelta

from config.settings import CITIES

from services.api import fetch_air_quality
from services.cleaning import clean_data

from database.db import (
    initialize_database,
    save_data,
    load_data
)

from components.layout import (
    apply_theme,
    render_header,
    render_footer
)

from components.charts import trend_chart


st.set_page_config(
    page_title="AIRVISION",
    page_icon="🌍",
    layout="wide"
)

apply_theme()
initialize_database()

st.sidebar.markdown("# 🌍 AIRVISION")
st.sidebar.caption("ENVIRONMENTAL INTELLIGENCE")

st.sidebar.divider()

city = st.sidebar.selectbox(
    "Select City",
    list(CITIES.keys()),
    index=0
)

period = st.sidebar.selectbox(
    "Historical Period",
    ["7 days", "30 days", "90 days", "1 year"]
)

days = {
    "7 days": 7,
    "30 days": 30,
    "90 days": 90,
    "1 year": 365
}[period]

today = date.today()
start_date = today - timedelta(days=days)

if st.sidebar.button(
    "FETCH REAL DATA",
    use_container_width=True
):

    try:

        with st.spinner("Loading air quality data..."):

            raw = fetch_air_quality(
                city,
                start_date,
                today
            )

            clean, report = clean_data(raw)

            inserted = save_data(clean)

            st.session_state["quality_report"] = report

            st.session_state["active_data"] = clean

            st.session_state["active_city"] = city

            st.success(
                f"Retrieved {len(clean)} records. "
                f"Saved {inserted} new records."
            )

    except Exception as exc:

        st.error(f"API error: {exc}")

if (
    "active_data" not in st.session_state
    or st.session_state.get("active_city") != city
):

    stored = load_data(city)

    if not stored.empty:

        stored = stored.rename(columns={
            "date": "Date",
            "city": "City",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "pm25": "PM2.5",
            "pm10": "PM10",
            "no2": "NO2",
            "co": "CO",
            "so2": "SO2",
            "o3": "O3",
            "european_aqi": "European AQI",
            "us_aqi": "US AQI"
        })

        stored, report = clean_data(stored)

        st.session_state["active_data"] = stored
        st.session_state["active_city"] = city
        st.session_state["quality_report"] = report

if "active_data" not in st.session_state:

    render_header()

    st.info(
        "Select a city and press FETCH REAL DATA "
        "to begin exploring AIRVISION."
    )

    render_footer()
    st.stop()

df = st.session_state["active_data"].copy()

if df.empty:
    st.warning("No observations available.")
    st.stop()

render_header()

st.caption(
    f"Location: {city} | "
    f"Observations: {len(df):,}"
)

pollutant = st.selectbox(
    "Main pollutant",
    [
        col for col in [
            "PM2.5", "PM10", "NO2",
            "CO", "SO2", "O3",
            "European AQI", "US AQI"
        ]
        if col in df.columns
    ]
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "PM2.5 Average",
    f"{df['PM2.5'].mean():.2f} µg/m³"
)

k2.metric(
    "PM10 Average",
    f"{df['PM10'].mean():.2f} µg/m³"
)

k3.metric(
    "European AQI",
    f"{df['European AQI'].mean():.1f}"
)

k4.metric(
    "Observations",
    f"{len(df):,}"
)

st.divider()

st.subheader("📈 Pollution Trends")

st.plotly_chart(
    trend_chart(df, pollutant),
    use_container_width=True
)

st.subheader("Dataset Preview")

st.dataframe(
    df.sort_values(
        "Date",
        ascending=False
    ).head(100),
    use_container_width=True
)

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    file_name="airvision_data.csv",
    mime="text/csv"
)

render_footer()
