import pandas as pd

df = pd.read_csv("output/parking_occupancy_summary.csv")

print(df["SystemCodeNumber"].tolist())