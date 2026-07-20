import pandas as pd

# ==========================
# Load Filtered Occupancy Data
# ==========================
df = pd.read_csv("output/occupancy_filtered.csv")

print("Total Records:", len(df))

# ==========================
# Convert Timestamp
# ==========================
df["LastUpdated"] = pd.to_datetime(df["LastUpdated"])

# Extract Hour and Day
df["Hour"] = df["LastUpdated"].dt.hour
df["DayOfWeek"] = df["LastUpdated"].dt.day_name()

# ==========================
# Feature Engineering
# ==========================
summary = (
    df.groupby("SystemCodeNumber")
      .agg(
          Capacity=("Capacity", "first"),
          AvgOccupancy=("Occupancy", "mean"),
          MaxOccupancy=("Occupancy", "max"),
          MinOccupancy=("Occupancy", "min"),
          StdOccupancy=("Occupancy", "std")
      )
      .reset_index()
)

# Occupancy Ratio
summary["OccupancyRatio"] = (
    (summary["AvgOccupancy"] / summary["Capacity"]) * 100
).round(2)

def utilization_level(ratio):
    if ratio < 30:
        return "Low"
    elif ratio < 60:
        return "Moderate"
    elif ratio < 80:
        return "High"
    else:
        return "Critical"

summary["UtilizationLevel"] = summary["OccupancyRatio"].apply(utilization_level)

# ==========================
# Peak Hour
# ==========================
peak_hour = (
    df.groupby(["SystemCodeNumber", "Hour"])
      .Occupancy.mean()
      .reset_index()
)

peak_hour = (
    peak_hour.sort_values(
        "Occupancy",
        ascending=False
    )
    .drop_duplicates("SystemCodeNumber")
)

summary = summary.merge(
    peak_hour[["SystemCodeNumber", "Hour"]],
    on="SystemCodeNumber"
)

summary.rename(
    columns={"Hour": "PeakHour"},
    inplace=True
)

# ==========================
# Peak Day
# ==========================
peak_day = (
    df.groupby(["SystemCodeNumber", "DayOfWeek"])
      .Occupancy.mean()
      .reset_index()
)

peak_day = (
    peak_day.sort_values(
        "Occupancy",
        ascending=False
    )
    .drop_duplicates("SystemCodeNumber")
)

summary = summary.merge(
    peak_day[["SystemCodeNumber", "DayOfWeek"]],
    on="SystemCodeNumber"
)

summary.rename(
    columns={
        "DayOfWeek": "PeakDay"
    },
    inplace=True
)

# ==========================
# Save
# ==========================
summary.to_csv(
    "output/parking_features.csv",
    index=False
)

print("\nFeature Engineering Completed!\n")

print(summary.head())

print("\nParking Locations:", len(summary))