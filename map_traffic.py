import pandas as pd
from scipy.spatial import KDTree

# ======================================
# Load Data
# ======================================
parking = pd.read_csv("output/parking_master.csv")
traffic = pd.read_csv("output/birmingham_traffic.csv")

print("Parking Locations :", len(parking))
print("Traffic Points    :", len(traffic))

# ======================================
# Build KDTree
# ======================================
traffic_coords = traffic[["latitude", "longitude"]].values
tree = KDTree(traffic_coords)

# ======================================
# Find Nearest Traffic Point
# ======================================
parking_coords = parking[["Latitude", "Longitude"]].values

distance, index = tree.query(parking_coords)

# ======================================
# Attach Traffic Information
# ======================================
parking["NearestCountPoint"] = traffic.iloc[index]["count_point_id"].values
parking["NearestRoad"] = traffic.iloc[index]["road_name"].values
parking["VehicleCount"] = traffic.iloc[index]["all_motor_vehicles"].values
parking["TrafficLevel"] = traffic.iloc[index]["TrafficLevel"].values

# Distance in degrees (temporary)
parking["DistanceDegrees"] = distance

# ======================================
# Save
# ======================================
parking.to_csv(
    "output/parking_master_with_traffic.csv",
    index=False
)

print("\nTraffic Mapping Completed!\n")

print(parking[[
    "ParkingName",
    "NearestRoad",
    "VehicleCount",
    "TrafficLevel"
]].head())

print("\nSaved Successfully!")