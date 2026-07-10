import osmnx as ox

tags = {"amenity": "parking"}

gdf = ox.features_from_place(
    "Birmingham, UK",
    tags
)

gdf["latitude"] = gdf.geometry.centroid.y
gdf["longitude"] = gdf.geometry.centroid.x

parking = gdf[["name","latitude","longitude"]]

parking.to_csv("parking.csv", index=False)

print(parking.head())