import pandas as pd

# Read CSV
df = pd.read_csv("raw_locations.csv")

# Keep required columns
df = df[["SystemCodeNumber", "Parking Name", "Latitude", "Longitude"]]

# Rename column
df.rename(columns={"Parking Name": "ParkingName"}, inplace=True)

# Clean parking names (removes hidden Unicode characters)
df["ParkingName"] = (
    df["ParkingName"]
    .astype(str)
    .str.replace("\u2060", "", regex=False)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

# Clean Latitude
df["Latitude"] = (
    df["Latitude"]
    .astype(str)
    .str.replace("° N", "", regex=False)
    .str.replace("° S", "-", regex=False)
    .str.replace("N/A", "", regex=False)
    .str.replace("TBD", "", regex=False)
    .str.strip()
)

# Clean Longitude
df["Longitude"] = (
    df["Longitude"]
    .astype(str)
    .str.replace("° E", "", regex=False)
    .str.replace("° W", "", regex=False)   # already negative in your file
    .str.replace("N/A", "", regex=False)
    .str.replace("TBD", "", regex=False)
    .str.strip()
)

# Convert to numbers
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# Save cleaned file
df.to_csv("data/parking_locations.csv", index=False)

print(df.head())
print("\nRows:", len(df))
print("Mapped:", df["Latitude"].notna().sum())
print("Unmapped:", df["Latitude"].isna().sum())