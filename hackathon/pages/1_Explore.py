
import streamlit as st

from components.charts import (
    trend_chart,
    correlation_chart
)

from services.analytics import (
    calculate_correlation,
    calculate_moving_average
)


st.set_page_config(
    page_title="Explore | AIRVISION",
    layout="wide"
)

st.title("🔎 Data Explorer")

if "active_data" not in st.session_state:
    st.warning("Load data from the main dashboard first.")
    st.stop()

df = st.session_state["active_data"].copy()

pollutants = [
    col for col in [
        "PM2.5", "PM10", "NO2",
        "CO", "SO2", "O3",
        "European AQI", "US AQI"
    ]
    if col in df.columns
]

city = st.selectbox(
    "Select city",
    sorted(df["City"].unique())
)

city_data = df[df["City"] == city].copy()

selected = st.multiselect(
    "Select pollutants",
    pollutants,
    default=pollutants[:4]
)

for pollutant in selected:

    st.plotly_chart(
        trend_chart(city_data, pollutant),
        use_container_width=True
    )

st.divider()

st.subheader("Correlation Matrix")

correlation = calculate_correlation(city_data)

st.plotly_chart(
    correlation_chart(correlation),
    use_container_width=True
)

st.divider()

st.subheader("Moving Average")

pollutant = st.selectbox(
    "Choose pollutant",
    pollutants,
    key="moving_pollutant"
)

window = st.slider(
    "Window",
    3, 168, 24
)

moving = calculate_moving_average(
    city_data,
    pollutant,
    window
)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=moving["Date"],
        y=moving[pollutant],
        name="Original"
    )
)

fig.add_trace(
    go.Scatter(
        x=moving["Date"],
        y=moving["Moving Average"],
        name="Moving Average"
    )
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(city_data, use_container_width=True)
