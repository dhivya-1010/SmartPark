import pandas as pd

traffic = pd.read_csv("data/dft_traffic_counts_aadf_by_direction.csv")

print(traffic.columns.tolist())
print()
print(traffic.head())
print()
print("Rows:", len(traffic))