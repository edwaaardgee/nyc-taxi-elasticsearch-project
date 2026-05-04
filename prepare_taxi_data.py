import pandas as pd
import os

# Load the original NYC Yellow Taxi data
file_path = r"C:\Users\[yourname]\Downloads\yellow_tripdata_2026-03.parquet"
df = pd.read_parquet(file_path)

# Keep only the columns needed for the project
columns_needed = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "total_amount"
]

df = df[columns_needed]

# Remove missing values and invalid trips
df = df.dropna()
df = df[df["trip_distance"] > 0]
df = df[df["fare_amount"] > 0]
df = df[df["total_amount"] > 0]

# Create extra columns for analysis
df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
df["pickup_day"] = df["tpep_pickup_datetime"].dt.day

df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

# Remove trips with unrealistic duration
df = df[df["trip_duration_minutes"] > 0]
df = df[df["trip_duration_minutes"] < 180]

# Create a smaller sample for Elasticsearch
df_sample = df.sample(n=150000, random_state=42)

# Save the cleaned dataset
output_file = r"C:\Users\[yourname]\Downloads\nyc_taxi_subset.csv"
df_sample.to_csv(output_file, index=False)

# Print final results
size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("Rows:", len(df_sample))
print(f"File size: {size_mb:.2f} MB")
print("Saved file:", output_file)
