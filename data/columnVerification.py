import pandas as pd

# Read dataset
df = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

# Filter Birmingham and latest year
birmingham = df[
    (df["local_authority_name"] == "Birmingham") &
    (df["year"] == 2025)
]

# Aggregate both directions
traffic = (
    birmingham
    .groupby(
        ["road_name", "latitude", "longitude"],
        as_index=False
    )["all_motor_vehicles"]
    .sum()
)

print("Unique Traffic Points:", len(traffic))
print(traffic.head())