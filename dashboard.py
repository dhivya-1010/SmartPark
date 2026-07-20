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
# Load Data
# ======================================
df = pd.read_csv("output/final_decision_intelligence.csv")

# ======================================
# Dashboard Title
# ======================================
st.title("🏛️ Government Decision Intelligence Dashboard")
st.markdown("Decision Support System for Urban Parking Management")

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
# Parking Data
# ======================================
st.subheader("Parking Facilities")

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