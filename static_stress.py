import pandas as pd

# Load occupancy dataset
df = pd.read_csv("data/occupancy_dataset.csv")

# Calculate average occupancy for each parking location
parking = (
    df.groupby("SystemCodeNumber")
    .agg({
        "Capacity": "first",
        "Occupancy": "mean"
    })
    .reset_index()
)

# Calculate occupancy ratio
parking["occupancy_ratio"] = parking["Occupancy"] / parking["Capacity"]

# Static Stress (60% weight)
parking["static_stress"] = parking["occupancy_ratio"] * 0.6

# Static Stress Percentage
parking["static_stress_percent"] = (
    parking["static_stress"] * 100
).round(2)


# Classify Stress Level
def classify(stress):
    if stress < 0.15:
        return "Low"
    elif stress < 0.30:
        return "Medium"
    elif stress < 0.45:
        return "High"
    else:
        return "Critical"


parking["static_stress_level"] = parking["static_stress"].apply(classify)

# Display Result
print("\n========== STATIC STRESS ANALYSIS ==========\n")

print(
    parking[
        [
            "SystemCodeNumber",
            "Capacity",
            "Occupancy",
            "occupancy_ratio",
            "static_stress_percent",
            "static_stress_level"
        ]
    ]
)

# Save output
parking.to_csv(
    "output/static_stress.csv",
    index=False
)

print("\nStatic stress analysis saved to output/static_stress.csv")
print("\nDone.")