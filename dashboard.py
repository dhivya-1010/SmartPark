import streamlit as st
import pandas as pd

# ======================================
# Page Configuration
# ======================================
st.set_page_config(
    page_title="Government Decision Intelligence Dashboard",
    page_icon="🏛️",
    layout="wide"
)

# ======================================
# Sidebar Navigation
# ======================================
st.sidebar.title("🏛️ UDIP")
st.sidebar.caption("Urban Decision Intelligence Platform")

st.sidebar.markdown("---")

st.sidebar.subheader("Navigation")

selected = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "📊 Parking Analysis",
        "🗺️ Traffic Intelligence",
        "🚦 Decision Engine",
        "📑 Reports"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("System Status")
st.sidebar.success("🟢 Decision Engine Online")
st.sidebar.info("Dataset Loaded")
st.sidebar.write(f"Parking Facilities : **22**")

st.sidebar.markdown("---")
st.sidebar.caption("Government Decision Support System")

# ======================================
# Load Data
# ======================================
df = pd.read_csv("output/final_decision_intelligence.csv")

# ======================================
# Dashboard Page
# ======================================
if selected == "🏠 Dashboard":

    st.title("🏛️ Government Decision Intelligence Dashboard")
    st.markdown("### Decision Support System for Urban Parking Management")

    st.divider()

    # ======================================
    # KPI Calculations
    # ======================================
    total = len(df)
    critical = (df["Priority"] == "Critical").sum()
    high = (df["Priority"] == "High").sum()
    moderate = (df["Priority"] == "Moderate").sum()
    low = (df["Priority"] == "Low").sum()

    # ======================================
    # KPI Cards
    # ======================================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Parking Facilities", total)
    col2.metric("Critical", critical)
    col3.metric("High", high)
    col4.metric("Moderate", moderate)
    col5.metric("Low", low)

    st.divider()

    # ======================================
    # Parking Table
    # ======================================
    st.subheader("📋 Parking Facilities")

    st.dataframe(
        df[
            [
                "ParkingName",
                "Priority",
                "SystemicStress",
                "Reason"
            ]
        ],
        use_container_width=True
    )

# ======================================
# Placeholder Pages
# ======================================

elif selected == "📊 Parking Analysis":

    st.title("📊 Parking Analysis")
    st.info("Module under development.")

elif selected == "🗺️ Traffic Intelligence":

    st.title("🗺️ Traffic Intelligence")
    st.info("Module under development.")

elif selected == "🚦 Decision Engine":

    st.title("🚦 Decision Engine")
    st.info("Module under development.")

elif selected == "📑 Reports":

    st.title("📑 Reports")
    st.info("Module under development.")