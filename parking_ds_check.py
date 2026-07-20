import pandas as pd

df = pd.read_csv("data/parking_locations.csv")

print(df.info())
print()
print(df.head())