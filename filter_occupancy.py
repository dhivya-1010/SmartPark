import pandas as pd

# ==========================
# Load Parking Locations
# ==========================
parking = pd.read_csv("data/parking_locations.csv")

print("Parking Locations:", len(parking))

# Keep only locations that have coordinates
parking = parking.dropna(subset=["Latitude", "Longitude"])

print("Mapped Parking Locations:", len(parking))

# Extract valid System Codes
valid_codes = parking["SystemCodeNumber"].unique()

print("Unique System Codes:", len(valid_codes))

# ==========================
# Load Occupancy Dataset
# ==========================
occupancy = pd.read_csv("data/occupancy_dataset.csv")

print("\nOriginal Occupancy Records:", len(occupancy))

# ==========================
# Filter Occupancy
# ==========================
filtered = occupancy[
    occupancy["SystemCodeNumber"].isin(valid_codes)
].copy()

print("Filtered Occupancy Records:", len(filtered))

print("Unique Parking Locations:", filtered["SystemCodeNumber"].nunique())

# ==========================
# Save Output
# ==========================
filtered.to_csv(
    "output/occupancy_filtered.csv",
    index=False
)

print("\nSaved Successfully!")
print("Output: output/occupancy_filtered.csv")