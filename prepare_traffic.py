import pandas as pd

print("Loading UK Traffic Dataset...")

# Load dataset
traffic = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

print("Original Records :", len(traffic))

# ======================================
# Filter Birmingham
# ======================================
traffic = traffic[
    traffic["local_authority_name"].str.contains(
        "Birmingham",
        case=False,
        na=False
    )
]

print("After Birmingham Filter :", len(traffic))

# ======================================
# Latest Available Year
# ======================================
latest_year = traffic["year"].max()

traffic = traffic[
    traffic["year"] == latest_year
]

print("Latest Year :", latest_year)
print("Records :", len(traffic))

# ======================================
# Aggregate Both Directions
# ======================================
traffic = (
    traffic.groupby(
        [
            "count_point_id",
            "road_name",
            "latitude",
            "longitude"
        ],
        as_index=False
    )
    .agg(
        {
            "all_motor_vehicles": "sum"
        }
    )
)

print("Unique Traffic Points :", len(traffic))

# ======================================
# Traffic Level
# ======================================
q1 = traffic["all_motor_vehicles"].quantile(0.25)
q2 = traffic["all_motor_vehicles"].quantile(0.50)
q3 = traffic["all_motor_vehicles"].quantile(0.75)

def classify(count):
    if count <= q1:
        return "Low"
    elif count <= q2:
        return "Medium"
    elif count <= q3:
        return "High"
    else:
        return "Very High"

traffic["TrafficLevel"] = traffic["all_motor_vehicles"].apply(classify)

# ======================================
# Save
# ======================================
traffic.to_csv(
    "output/birmingham_traffic.csv",
    index=False
)

print("\nSaved Successfully!")
print("Output : output/birmingham_traffic.csv")

print("\nPreview:\n")
print(traffic.head())