import pandas as pd
import folium
from folium.plugins import HeatMap

# -------------------------------
# Load Parking Dataset
# -------------------------------
parking = pd.read_csv("data/parking.csv")

# -------------------------------
# Load Traffic Dataset
# -------------------------------
traffic = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

# -------------------------------
# Filter Birmingham + 2025
# -------------------------------
traffic = traffic[
    (traffic["local_authority_name"] == "Birmingham") &
    (traffic["year"] == 2025)
]

# -------------------------------
# Aggregate both directions
# -------------------------------
traffic = (
    traffic
    .groupby(
        ["road_name", "latitude", "longitude"],
        as_index=False
    )["all_motor_vehicles"]
    .sum()
)

# -------------------------------
# Create Base Map
# -------------------------------
m = folium.Map(
    location=[52.4862, -1.8904],
    zoom_start=12
)

# -------------------------------
# Feature Groups
# -------------------------------
parking_layer = folium.FeatureGroup(name="Parking Areas")

traffic_layer = folium.FeatureGroup(name="Traffic Intensity")

# -------------------------------
# Parking Markers
# -------------------------------
for _, row in parking.iterrows():

    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
        continue

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=row["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(parking_layer)

# -------------------------------
# Traffic Circles
# -------------------------------
heat_data = []

max_vehicle = traffic["all_motor_vehicles"].max()

for _, row in traffic.iterrows():

    radius = (row["all_motor_vehicles"] / max_vehicle) * 20 + 3

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=radius,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.6,
        popup=f"""
        <b>Road:</b> {row['road_name']}<br>
        <b>Vehicles:</b> {int(row['all_motor_vehicles'])}
        """
    ).add_to(traffic_layer)

    heat_data.append([
        row["latitude"],
        row["longitude"],
        row["all_motor_vehicles"]
    ])

# -------------------------------
# Heatmap
# -------------------------------
HeatMap(
    heat_data,
    name="Traffic Heatmap",
    radius=18,
    blur=12
).add_to(m)

# -------------------------------
# Add Layers
# -------------------------------
parking_layer.add_to(m)
traffic_layer.add_to(m)

folium.LayerControl().add_to(m)

# -------------------------------
# Save
# -------------------------------
m.save("maps/birmingham_map.html")

print("Map created successfully!")