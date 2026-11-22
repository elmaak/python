
import streamlit as st


def apply_theme():

    st.markdown("""
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap'
    );

    .stApp {
        background: #080d18;
        color: #edf3fc;
        font-family: Inter, sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #0c1422;
        border-right: 1px solid #25344b;
    }

    [data-testid="stMetric"] {
        background: #111b2b;
        border: 1px solid #25344b;
        border-radius: 14px;
        padding: 18px;
    }

    [data-testid="stMetricValue"] {
        color: #36d9ed;
        font-weight: 800;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(
            115deg, #10253a, #112039, #102e35
        );
        border: 1px solid #28455c;
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: 38px;
        font-weight: 800;
        color: white;
    }

    .hero p {
        color: #a5b8cc;
    }

    </style>
    """, unsafe_allow_html=True)


def render_header():

    st.markdown("""
    <div class="hero">
        <h1>🌍 AIRVISION</h1>
        <p>
            ADVANCED ENVIRONMENTAL INTELLIGENCE PLATFORM
        </p>
        <p>
            Explore atmospheric pollution.
            Analyze environmental patterns.
            Discover insights through data.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():

    st.divider()

    st.markdown("""
    <div style="
        text-align:center;
        color:#71839c;
        padding:15px;
    ">
        AIRVISION PROFESSIONAL EDITION<br>
        PYTHON · PANDAS · PLOTLY · SCIKIT-LEARN
    </div>
    """, unsafe_allow_html=True)
