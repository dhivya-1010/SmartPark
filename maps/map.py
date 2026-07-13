import pandas as pd
import folium
from folium.plugins import HeatMap

# -------------------------------
# Load Parking + Traffic Mapping
# -------------------------------
parking = pd.read_csv("output/parking_with_traffic.csv")

# -------------------------------
# Load Original Traffic Dataset
# -------------------------------
traffic = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

# -------------------------------
# Filter Birmingham (2025)
# -------------------------------
traffic = traffic[
    (traffic["local_authority_name"] == "Birmingham") &
    (traffic["year"] == 2025)
]

# -------------------------------
# Aggregate Both Directions
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
    zoom_start=12,
    tiles="OpenStreetMap"
)

# -------------------------------
# Layers
# -------------------------------
parking_layer = folium.FeatureGroup(name="Parking Areas")
traffic_layer = folium.FeatureGroup(name="Traffic Count Points")

# -------------------------------
# Parking Markers
# -------------------------------
for _, row in parking.iterrows():

    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
        continue

    # Blue Parking Marker
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"""
        <b>{row['name']}</b><br>
        <b>Nearest Road:</b> {row['nearest_road']}<br>
        <b>Vehicle Count:</b> {int(row['vehicle_count'])}<br>
        <b>Traffic Level:</b> {row['traffic_level']}
        """,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(parking_layer)

    # Highlight Potential Mismatch
    if row["vehicle_count"] >= 25000:

        folium.Circle(
            location=[row["latitude"], row["longitude"]],
            radius=80,
            color="yellow",
            weight=3,
            fill=True,
            fill_color="yellow",
            fill_opacity=0.35,
            popup=f"""
            <b>Potential Congestion Hotspot</b><br>
            Parking : {row['name']}<br>
            Vehicle Count : {int(row['vehicle_count'])}
            """
        ).add_to(parking_layer)

# -------------------------------
# Traffic Points
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
        fill_opacity=0.7,
        popup=f"""
        <b>Road:</b> {row['road_name']}<br>
        <b>Vehicle Count:</b> {int(row['all_motor_vehicles'])}
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
    radius=18,
    blur=12,
    min_opacity=0.4
).add_to(m)

# -------------------------------
# Add Layers
# -------------------------------
parking_layer.add_to(m)
traffic_layer.add_to(m)

folium.LayerControl().add_to(m)

# -------------------------------
# Save Map
# -------------------------------
m.save("maps/birmingham_map.html")

print("=" * 60)
print("Birmingham Decision Intelligence Map Created Successfully!")
print("=" * 60)
print(f"Parking Locations          : {len(parking)}")
print(f"Traffic Count Points       : {len(traffic)}")
print(f"Potential Hotspots (>25000): {len(parking[parking['vehicle_count'] >= 25000])}")

print("\nTop 10 High Traffic Parking Areas:\n")

top10 = parking.sort_values(
    by="vehicle_count",
    ascending=False
).head(10)

print(
    top10[
        [
            "name",
            "nearest_road",
            "vehicle_count",
            "traffic_level"
        ]
    ]
)

print("\nMap saved to:")
print("maps/birmingham_map.html")