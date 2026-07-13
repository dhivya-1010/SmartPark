import pandas as pd
from scipy.spatial import KDTree

# ----------------------------------------
# Load Parking Dataset
# ----------------------------------------
parking = pd.read_csv("data/parking.csv")

# Keep only named parking locations
parking = parking.dropna(subset=["name"])

# Remove rows with missing coordinates
parking = parking.dropna(subset=["latitude", "longitude"])

# ----------------------------------------
# Load Traffic Dataset
# ----------------------------------------
traffic = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

# ----------------------------------------
# Filter Birmingham (2025)
# ----------------------------------------
traffic = traffic[
    (traffic["local_authority_name"] == "Birmingham") &
    (traffic["year"] == 2025)
]

# ----------------------------------------
# Aggregate both travel directions
# ----------------------------------------
traffic = (
    traffic
    .groupby(
        ["road_name", "latitude", "longitude"],
        as_index=False
    )["all_motor_vehicles"]
    .sum()
)

print(f"Parking Locations : {len(parking)}")
print(f"Traffic Points    : {len(traffic)}")

# ----------------------------------------
# Build KDTree
# ----------------------------------------
traffic_coordinates = traffic[["latitude", "longitude"]].values
tree = KDTree(traffic_coordinates)

# ----------------------------------------
# Find nearest traffic point
# ----------------------------------------
parking_coordinates = parking[["latitude", "longitude"]].values
distance, index = tree.query(parking_coordinates)

# ----------------------------------------
# Attach nearest traffic information
# ----------------------------------------
parking["nearest_road"] = traffic.iloc[index]["road_name"].values
parking["vehicle_count"] = traffic.iloc[index]["all_motor_vehicles"].values
parking["distance"] = distance

# ----------------------------------------
# Traffic Level
# ----------------------------------------
def classify(vehicle_count):

    if vehicle_count >= 40000:
        return "Very High"
    elif vehicle_count >= 25000:
        return "High"
    elif vehicle_count >= 10000:
        return "Medium"
    else:
        return "Low"

parking["traffic_level"] = parking["vehicle_count"].apply(classify)

# ----------------------------------------
# Dynamic Throughput Component (40%)
# ----------------------------------------
max_vehicle = parking["vehicle_count"].max()

parking["dynamic_stress"] = (
    parking["vehicle_count"] / max_vehicle
) * 0.4

parking["dynamic_stress_percent"] = (
    parking["dynamic_stress"] * 100
).round(2)

# ----------------------------------------
# Static Storage Component (Future)
# ----------------------------------------
parking["static_stress"] = 0.0
parking["static_stress_percent"] = 0.0

# ----------------------------------------
# Systemic Stress Index
# ----------------------------------------
parking["systemic_stress"] = (
    parking["static_stress"] +
    parking["dynamic_stress"]
)

parking["systemic_stress_percent"] = (
    parking["systemic_stress"] * 100
).round(2)

# ----------------------------------------
# Priority Assignment
# ----------------------------------------
def assign_priority(stress):

    if stress >= 80:
        return "P1"

    elif stress >= 60:
        return "P2"

    elif stress >= 40:
        return "P3"

    else:
        return "P4"

parking["priority"] = parking["systemic_stress_percent"].apply(assign_priority)

# ----------------------------------------
# Municipal Action
# ----------------------------------------
def recommend_action(priority):

    if priority == "P1":
        return "Infrastructure Expansion"

    elif priority == "P2":
        return "Redirect Overflow"

    elif priority == "P3":
        return "Monitor"

    else:
        return "No Immediate Action"

parking["recommended_action"] = parking["priority"].apply(recommend_action)

# ----------------------------------------
# Save Output
# ----------------------------------------
parking.to_csv(
    "output/parking_with_traffic.csv",
    index=False
)

print("\nDone!")
print("Output saved to: output/parking_with_traffic.csv\n")

print(
    parking[
        [
            "name",
            "nearest_road",
            "vehicle_count",
            "traffic_level",
            "dynamic_stress_percent",
            "systemic_stress_percent",
            "priority",
            "recommended_action"
        ]
    ].head(10)
)