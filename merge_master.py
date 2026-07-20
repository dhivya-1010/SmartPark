import pandas as pd

# Load datasets
locations = pd.read_csv("data/parking_locations.csv")
features = pd.read_csv("output/parking_features.csv")

print("Locations :", len(locations))
print("Features  :", len(features))

# Keep only mapped locations
locations = locations.dropna(subset=["Latitude", "Longitude"])

# Merge
master = pd.merge(
    locations,
    features,
    on="SystemCodeNumber",
    how="inner"
)

print("\nMaster Dataset Rows :", len(master))

# Save
master.to_csv(
    "output/parking_master.csv",
    index=False
)

print("\nSaved Successfully!")
print(master.head())