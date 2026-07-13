import pandas as pd

df = pd.read_csv("output/parking_with_traffic.csv")

print(df["traffic_level"].value_counts())