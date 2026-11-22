
import plotly.express as px
import plotly.graph_objects as go


DARK_TEMPLATE = "plotly_dark"

COLORS = [
    "#36d9ed",
    "#22d3a6",
    "#ffb84d",
    "#a78bfa",
    "#fb7185",
    "#60a5fa"
]


def trend_chart(df, pollutant):

    fig = px.line(
        df,
        x="Date",
        y=pollutant,
        color="City",
        color_discrete_sequence=COLORS,
        template=DARK_TEMPLATE,
        title=f"{pollutant} — Pollution Trend"
    )

    fig.update_layout(
        hovermode="x unified",
        paper_bgcolor="#111b2b",
        plot_bgcolor="#111b2b"
    )

    return fig


def comparison_chart(df, pollutant):

    fig = px.bar(
        df,
        x="City",
        y=pollutant,
        color=pollutant,
        color_continuous_scale="Tealgrn",
        template=DARK_TEMPLATE,
        title=f"Average {pollutant} by City"
    )

    return fig


def correlation_chart(correlation):

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        template=DARK_TEMPLATE,
        title="Pollutant Correlation Matrix"
    )

    return fig


def forecast_chart(historical, future, pollutant):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical.index,
            y=historical.values,
            name="Historical",
            line=dict(color="#36d9ed")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future["Date"],
            y=future["Forecast"],
            name="Forecast",
            line=dict(
                color="#ffb84d",
                width=3,
                dash="dash"
            )
        )
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        title=f"{pollutant} Forecast",
        paper_bgcolor="#111b2b",
        plot_bgcolor="#111b2b",
        hovermode="x unified"
    )

    return fig


def anomaly_chart(df, pollutant):

    fig = px.scatter(
        df,
        x="Date",
        y=pollutant,
        color="Status",
        hover_data=["City"],
        color_discrete_map={
            "Normal": "#22d3a6",
            "Anomaly": "#fb7185"
        },
        template=DARK_TEMPLATE,
        title="Pollution Anomaly Detection"
    )

    return fig
