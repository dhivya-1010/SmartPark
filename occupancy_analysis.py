import pandas as pd

# Load dataset
df = pd.read_csv("data/occupancy_dataset.csv")

# Historical occupancy for each parking system
parking_occ = (
    df.groupby("SystemCodeNumber")
      .agg({
          "Capacity": "first",
          "Occupancy": "mean"
      })
      .reset_index()
)

parking_occ["Occupancy"] = parking_occ["Occupancy"].round(2)

print(parking_occ)

print("\nNumber of parking systems:", len(parking_occ))

# Save for later use
parking_occ.to_csv(
    "output/parking_occupancy_summary.csv",
    index=False
)

print("\nSaved to output/parking_occupancy_summary.csv")