import pandas as pd
import geopandas as gpd
import os

# Load cleaned taxi data
taxi_file = "nyc_taxi_subset.csv"
df = pd.read_csv(taxi_file)

# Load NYC taxi zone shapefile
zones_file = "taxi_zones/taxi_zones.shp"
zones = gpd.read_file(zones_file)

# Convert taxi zones into latitude/longitude center points
zones = zones.to_crs(epsg=2263)
zones["centroid"] = zones.geometry.centroid

zone_points = gpd.GeoDataFrame(
    zones[["LocationID", "zone", "borough"]],
    geometry=zones["centroid"],
    crs="EPSG:2263"
).to_crs(epsg=4326)

zone_points["longitude"] = zone_points.geometry.x
zone_points["latitude"] = zone_points.geometry.y

zone_points = zone_points[[
    "LocationID",
    "zone",
    "borough",
    "longitude",
    "latitude"
]]

# Add pickup location information
df = df.merge(
    zone_points,
    left_on="PULocationID",
    right_on="LocationID",
    how="left"
)

df = df.rename(columns={
    "zone": "pickup_zone",
    "borough": "pickup_borough",
    "longitude": "pickup_longitude",
    "latitude": "pickup_latitude"
})

df = df.drop(columns=["LocationID"])

# Add dropoff location information
df = df.merge(
    zone_points,
    left_on="DOLocationID",
    right_on="LocationID",
    how="left"
)

df = df.rename(columns={
    "zone": "dropoff_zone",
    "borough": "dropoff_borough",
    "longitude": "dropoff_longitude",
    "latitude": "dropoff_latitude"
})

df = df.drop(columns=["LocationID"])

# Remove rows without location data
df = df.dropna(subset=[
    "pickup_latitude",
    "pickup_longitude",
    "dropoff_latitude",
    "dropoff_longitude"
])

# Create geo-point fields for Kibana Maps
df["pickup_location"] = (
    df["pickup_latitude"].astype(str) + "," + df["pickup_longitude"].astype(str)
)

df["dropoff_location"] = (
    df["dropoff_latitude"].astype(str) + "," + df["dropoff_longitude"].astype(str)
)

# Keep file size within the project range
df = df.sample(n=100000, random_state=42)

# Save geo-enhanced file
output_file = "nyc_taxi_subset_with_geo.csv"
df.to_csv(output_file, index=False)

size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("Rows:", len(df))
print(f"File size: {size_mb:.2f} MB")
print("Saved file:", output_file)
