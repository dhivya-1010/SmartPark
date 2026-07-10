import pandas as pd

df = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

birmingham = df[df["local_authority_name"] == "Birmingham"]

print("Number of Birmingham records:", len(birmingham))

print(birmingham[[
    "road_name",
    "latitude",
    "longitude",
    "all_motor_vehicles",
    "year"
]].head())

birmingham = birmingham[birmingham["year"] == 2025]

print("2025 Records:", len(birmingham))

print(birmingham[[
    "road_name",
    "latitude",
    "longitude",
    "all_motor_vehicles"
]].head())