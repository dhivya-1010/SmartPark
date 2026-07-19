import pandas as pd

# Load occupancy dataset
df = pd.read_csv("data/occupancy_dataset.csv")   # Change filename if needed

print(df.head())

print("\nColumns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nUnique Parking Systems:")
print(df["SystemCodeNumber"].nunique())