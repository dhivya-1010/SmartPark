import pandas as pd

df = pd.read_csv(
    "data/dft_traffic_counts_aadf_by_direction.csv",
    low_memory=False
)

print(df["local_authority_name"].unique())