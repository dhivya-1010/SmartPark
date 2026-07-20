# ParkIQ – Community Parking Intelligence for Urban Mobility

> **A Decision Intelligence platform for data-driven urban parking and traffic management.**

ParkIQ is a government-oriented Decision Intelligence platform that transforms static parking and traffic datasets into actionable insights for urban planners and city administrators. Instead of merely visualizing traffic or parking locations, ParkIQ analyzes the relationship between parking infrastructure and surrounding traffic intensity to identify congestion hotspots, prioritize intervention areas, and recommend strategic actions.

The platform demonstrates how data integration, spatial analytics, and decision intelligence can support smarter urban mobility planning without requiring expensive sensor deployments.

---

# Live Demo

**Streamlit Dashboard:** https://parkiq.streamlit.app/

---

# Project Overview

Modern cities face increasing traffic congestion and inefficient utilization of parking infrastructure. While parking and traffic data are often available independently, governments frequently lack integrated decision-support systems capable of transforming these datasets into meaningful operational insights.

ParkIQ addresses this challenge by combining:

* Public parking datasets
* Official traffic count datasets
* Spatial nearest-road mapping
* Decision Intelligence algorithms
* Government-oriented visualization dashboards

The result is a unified platform that enables authorities to identify high-impact parking locations, evaluate congestion levels, and prioritize infrastructure planning.

---

# Objectives

The primary objectives of ParkIQ are:

* Integrate heterogeneous parking and traffic datasets.
* Analyze the relationship between parking demand and nearby traffic intensity.
* Generate interpretable urban stress indicators.
* Prioritize parking locations based on systemic congestion.
* Provide actionable recommendations for city administrators.
* Visualize decision-support insights through an interactive dashboard.

---

# Key Features

## Parking Intelligence

* Interactive parking location visualization
* Parking inventory exploration
* Geographic distribution analysis
* Location-specific metadata

---

## Traffic Intelligence

* Official traffic count integration
* Traffic intensity categorization
* Road-wise vehicle analysis
* Congestion hotspot identification

---

## Spatial Analytics

* Nearest-road mapping using KDTree
* Distance calculation between parking locations and traffic count stations
* Parking-to-road association
* Geographic enrichment of parking records

---

## Decision Intelligence Engine

The core decision engine evaluates parking locations using integrated traffic information and generates:

* Dynamic traffic stress
* Systemic Stress Index
* Parking priority classification
* Government recommendations

---

## Interactive GIS Dashboard

Features include:

* Interactive city map
* Heatmap visualization
* Color-coded parking markers
* Traffic intensity visualization
* Detailed location popups
* Filtering and exploration

---

## Executive Analytics

Dashboard components include:

* KPI Cards
* Priority Distribution
* Traffic Distribution
* Stress Distribution
* Critical Parking Locations
* Decision Summary

---

# Decision Intelligence Workflow

```text
Parking Dataset
        │
        ▼
Traffic Dataset
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Spatial Mapping (KDTree)
        │
        ▼
Traffic Association
        │
        ▼
Systemic Stress Calculation
        │
        ▼
Priority Classification
        │
        ▼
Recommendation Engine
        │
        ▼
Interactive Government Dashboard
```

---

# System Architecture

```text
                +-----------------------+
                | Parking Dataset       |
                +-----------------------+
                           |
                           |
                           ▼
                +-----------------------+
                | Traffic Dataset       |
                +-----------------------+
                           |
                           ▼
                +-----------------------+
                | Data Processing       |
                +-----------------------+
                           |
                           ▼
                +-----------------------+
                | Spatial Mapping       |
                | (KDTree)              |
                +-----------------------+
                           |
                           ▼
                +-----------------------+
                | Decision Engine       |
                +-----------------------+
                           |
                           ▼
                +-----------------------+
                | Recommendation Engine |
                +-----------------------+
                           |
                           ▼
                +-----------------------+
                | Streamlit Dashboard   |
                +-----------------------+
```

---

# Technology Stack

## Frontend

* Streamlit
* HTML
* CSS

## Backend

* Python

## Data Processing

* Pandas
* NumPy

## Geospatial Analytics

* SciPy KDTree
* Folium
* Streamlit-Folium

## Visualization

* Plotly
* Matplotlib

---

# Project Structure

```text
ParkIQ/
│
├── dashboard.py
├── requirements.txt
├── data/
│   ├── parking.csv
│   ├── traffic.csv
│   └── parking_with_traffic.csv
│
├── output/
│
├── assets/
│
├── screenshots/
│
└── README.md
```

---

# Data Sources

## Parking Dataset

Contains:

* Parking Name
* Latitude
* Longitude
* Parking Capacity
* Geographic Coordinates

## Traffic Dataset

Contains:

* Road Name
* Traffic Count
* Vehicle Volume
* Latitude
* Longitude

---

# Spatial Mapping

Each parking location is matched to the nearest traffic monitoring point using the KDTree nearest-neighbor algorithm.

This enables the platform to associate:

* Traffic volume
* Road information
* Distance
* Congestion level

with every parking location.

---

# Decision Intelligence

The platform computes traffic-driven stress metrics and classifies locations into actionable priority levels.

The generated indicators help identify:

* High-pressure parking zones
* Underutilized parking infrastructure
* Congestion hotspots
* Areas requiring intervention

---

# Priority Levels

| Priority | Description                    |
| -------- | ------------------------------ |
| P1       | Critical intervention required |
| P2       | High priority monitoring       |
| P3       | Moderate congestion            |
| P4       | Low priority                   |
| P5       | Normal operation               |

---

# Recommendation Engine

Based on the computed stress levels, ParkIQ recommends actions such as:

* Increase parking capacity
* Improve traffic flow
* Monitor congestion trends
* Deploy temporary traffic management
* Continue normal operations

These recommendations are intended to support decision-makers in prioritizing urban mobility interventions.

---

# Dashboard Highlights

The dashboard provides:

* Executive summary
* Interactive city map
* Parking hotspot visualization
* Heatmaps
* Traffic analysis
* Priority analytics
* Government recommendations
* Decision support insights

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/dhivya-1010/SmartPark.git
```

## Navigate

```bash
cd ParkIQ
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run dashboard.py
```

---

# Use Cases

ParkIQ can assist:

* Municipal Corporations
* Smart City Missions
* Urban Planning Authorities
* Transportation Departments
* Parking Operators
* Infrastructure Consultants
* Academic Research
* Urban Analytics Projects

---

# Future Enhancements

Potential extensions include:

* Real-time IoT parking sensors
* Live traffic feeds
* Predictive congestion forecasting
* Parking occupancy prediction
* Multi-city support
* Mobile application
* Route optimization
* Public transport integration
* Digital twin visualization
* AI-driven scenario simulation

---

# 👩‍💻 Author

**Dhivya V**

BE CSE
Sri Eshwar College of Engineering

---

# License

This project is intended for academic, research, and educational purposes.

---

# Acknowledgements

Special thanks to:

* Public parking and traffic data providers
* Open-source Python ecosystem
* Streamlit community
* Folium developers
* Pandas, NumPy, SciPy, and Plotly contributors

whose tools made this project possible.

---

## ParkIQ Vision

**"Transforming Urban Mobility through Data-Driven Decision Intelligence."**

ParkIQ demonstrates how integrated datasets, spatial analytics, and interpretable decision support can help city administrators move beyond descriptive dashboards toward evidence-based urban planning. By converting parking and traffic information into actionable insights, the platform provides a practical foundation for smarter, more efficient, and sustainable mobility management.
