
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Geospatial | AIRVISION",
    layout="wide"
)

st.title("🗺️ Geospatial Intelligence")

if "active_data" not in st.session_state:
    st.warning("Load data from dashboard first.")
    st.stop()

df = st.session_state["active_data"].copy()

pollutant = st.selectbox(
    "Choose indicator",
    ["PM2.5", "PM10", "European AQI"]
)

locations = (
    df.groupby("City")
    .agg(
        Latitude=("Latitude", "mean"),
        Longitude=("Longitude", "mean"),
        Pollution=(pollutant, "mean")
    )
    .dropna()
    .reset_index()
)

fig = px.scatter_map(
    locations,
    lat="Latitude",
    lon="Longitude",
    color="Pollution",
    size="Pollution",
    hover_name="City",
    color_continuous_scale="Turbo",
    zoom=3,
    map_style="open-street-map",
    title=f"{pollutant} Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    locations.sort_values(
        "Pollution",
        ascending=False
    ),
    use_container_width=True
)
