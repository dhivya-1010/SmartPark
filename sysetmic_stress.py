import pandas as pd

# ======================================
# Load Master Dataset
# ======================================
parking = pd.read_csv("output/parking_master_with_traffic.csv")

print("Parking Locations :", len(parking))

# ======================================
# Occupancy Score
# Already in percentage (0-100)
# ======================================
parking["OccupancyScore"] = parking["OccupancyRatio"]

# ======================================
# Traffic Score (Normalize 0-100)
# ======================================
min_vehicle = parking["VehicleCount"].min()
max_vehicle = parking["VehicleCount"].max()

parking["TrafficScore"] = (
    (parking["VehicleCount"] - min_vehicle)
    /
    (max_vehicle - min_vehicle)
) * 100

parking["TrafficScore"] = parking["TrafficScore"].round(2)

# ======================================
# Systemic Stress Index
# ======================================
parking["SystemicStress"] = (
    0.6 * parking["OccupancyScore"] +
    0.4 * parking["TrafficScore"]
).round(2)

# ======================================
# Priority Classification
# ======================================
def classify(stress):
    if stress < 30:
        return "Low"
    elif stress < 60:
        return "Moderate"
    elif stress < 80:
        return "High"
    else:
        return "Critical"

parking["Priority"] = parking["SystemicStress"].apply(classify)

# ======================================
# Save
# ======================================
parking.to_csv(
    "output/systemic_stress.csv",
    index=False
)

print("\nSystemic Stress Generated!\n")

print(
    parking[
        [
            "ParkingName",
            "OccupancyScore",
            "TrafficScore",
            "SystemicStress",
            "Priority"
        ]
    ].head()
)

print("\nSaved Successfully!")