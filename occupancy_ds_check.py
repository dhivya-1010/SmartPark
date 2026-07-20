import pandas as pd

df = pd.read_csv("data/occupancy_dataset.csv")

print(df.columns.tolist())
print()
print(df.head())