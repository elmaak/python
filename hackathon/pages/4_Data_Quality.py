
import streamlit as st
import plotly.express as px

from services.cleaning import (
    clean_data,
    detect_iqr_outliers
)


st.set_page_config(
    page_title="Data Quality | AIRVISION",
    layout="wide"
)

st.title("🧹 Data Quality Center")

if "active_data" not in st.session_state:
    st.warning("Load data from dashboard first.")
    st.stop()

df = st.session_state["active_data"].copy()

cleaned, report = clean_data(df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Original", report["original_rows"])
c2.metric("Cleaned", report["cleaned_rows"])
c3.metric("Duplicates", report["duplicates_removed"])
c4.metric("Missing", report["missing_total_after"])

st.divider()

st.subheader("Missing Values")

import pandas as pd

missing = pd.DataFrame({
    "Column": list(report["missing_before"].keys()),
    "Before": list(report["missing_before"].values()),
    "After": list(report["missing_after"].values())
})

fig = px.bar(
    missing,
    x="Column",
    y=["Before", "After"],
    barmode="group",
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Outlier Detection")

pollutants = [
    col for col in [
        "PM2.5", "PM10", "NO2",
        "CO", "SO2", "O3"
    ]
    if col in cleaned.columns
]

pollutant = st.selectbox(
    "Select pollutant",
    pollutants
)

outliers = detect_iqr_outliers(
    cleaned,
    pollutant
)

st.metric(
    "Potential Outliers",
    int(outliers.sum())
)

st.caption(
    "Statistical outliers are not automatically erroneous measurements."
)

st.dataframe(
    cleaned,
    use_container_width=True
)

st.download_button(
    "Download cleaned dataset",
    cleaned.to_csv(index=False),
    file_name="airvision_cleaned.csv",
    mime="text/csv"
)

st.json(report)
