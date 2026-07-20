import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# ======================================
# Page Configuration
# ======================================
st.set_page_config(
    page_title="Government Decision Intelligence Dashboard",
    page_icon="🏛️",
    layout="wide"
)

# ======================================
# Load Data
# ======================================
df = pd.read_csv("output/final_decision_intelligence.csv")

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
st.sidebar.write(f"Parking Facilities : **{len(df)}**")

st.sidebar.markdown("---")
st.sidebar.caption("Government Decision Support System")

# ======================================
# Dashboard
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
    col2.metric("🔴 Critical", critical)
    col3.metric("🟠 High", high)
    col4.metric("🟡 Moderate", moderate)
    col5.metric("🟢 Low", low)

    st.divider()

    # ======================================
    # Top Priority Parking
    # ======================================
    st.subheader("🏆 Top Priority Parking Locations")

    priority_order = {
        "Critical": 4,
        "High": 3,
        "Moderate": 2,
        "Low": 1
    }

    temp = df.copy()
    temp["PriorityRank"] = temp["Priority"].map(priority_order)

    top5 = (
        temp.sort_values(
            by=["PriorityRank", "SystemicStress"],
            ascending=[False, False]
        )
        .head(5)
    )

    st.dataframe(
        top5[
            [
                "ParkingName",
                "Priority",
                "SystemicStress",
                "ImmediateActions"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================
    # Interactive Map
    # ======================================
    st.subheader("🗺️ Urban Parking Intelligence Map")

    m = folium.Map(
        location=[52.4862, -1.8904],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    color_map = {
        "Critical": "red",
        "High": "orange",
        "Moderate": "blue",
        "Low": "green"
    }

    for _, row in df.iterrows():

        popup = f"""
        <h4>{row['ParkingName']}</h4>

        <b>Priority:</b> {row['Priority']}<br>

        <b>Systemic Stress:</b> {row['SystemicStress']:.2f}<br><br>

        <b>Reason</b><br>
        {row['Reason']}<br><br>

        <b>Immediate Actions</b><br>
        {row['ImmediateActions']}<br><br>

        <b>Long-Term Considerations</b><br>
        {row['LongTermConsiderations']}
        """

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=row["ParkingName"],
            popup=folium.Popup(popup, max_width=400),
            icon=folium.Icon(
                color=color_map.get(row["Priority"], "gray"),
                icon="car",
                prefix="fa"
            )
        ).add_to(m)

    st_folium(
        m,
        use_container_width=True,
        height=600
    )

    st.divider()

    # ======================================
    # Parking Facilities Table
    # ======================================
    st.subheader("📋 Parking Facilities")

    st.dataframe(
        df[
            [
                "ParkingName",
                "Priority",
                "SystemicStress",
                "TrafficLevel",
                "Reason"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# ======================================
# Parking Analysis
# ======================================
elif selected == "📊 Parking Analysis":

    st.title("📊 Parking Analysis")
    st.info("Module under development.")

# ======================================
# Traffic Intelligence
# ======================================
elif selected == "🗺️ Traffic Intelligence":

    st.title("🗺️ Traffic Intelligence")
    st.info("Module under development.")

# ======================================
# Decision Engine
# ======================================
elif selected == "🚦 Decision Engine":

    st.title("🚦 Decision Engine")
    st.info("Module under development.")

# ======================================
# Reports
# ======================================
elif selected == "📑 Reports":

    st.title("📑 Reports")
    st.info("Module under development.")