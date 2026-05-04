# NYC Taxi Trip Data Analysis Using Elasticsearch and Kibana

## Project Overview

This project analyzes NYC Yellow Taxi Trip Records using Elasticsearch, Kibana, and Python. The dataset was downloaded from the NYC Taxi and Limousine Commission. We cleaned and sampled the data, uploaded it into Elasticsearch, created Kibana visualizations, and built a geo-temporal map of taxi pickups.

## Data Source

NYC TLC Trip Record Data:  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Dataset used: Yellow Taxi Trip Records, March 2026.

## Platform Specs

- Platform: Elastic Cloud / Kibana
- Operating System: Windows 11
- Python Version: 3.13.13
- Libraries: pandas, pyarrow, geopandas
- Original dataset rows: 3,952,451
- Cleaned subset: 150,000 rows, 12.8 MB
- Geo subset: 100,000 rows, 28.2 MB
- Elasticsearch indexes: `nyc_taxi`, `nyc_taxi_geo2`

## How to Reproduce the Project

### Step 1: Download the Data

Go to the NYC TLC Trip Record Data page:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Download the March 2026 Yellow Taxi Trip Records file.

Expected file name:
yellow_tripdata_2026-03.parquet

### Step 2: Download the Taxi Zone Shapefile

On the same NYC TLC page, download the Taxi Zone Shapefile from the Taxi Zone Maps / Lookup Tables section.

Extract the ZIP file.

Expected shapefile path:
C:\Users\[yourname]\Downloads\taxi_zones\taxi_zones.shp

Replace [yourname] with the username on your own computer.

### Step 3: Install Python Libraries

Open Command Prompt or Terminal and run:
python -m pip install pandas pyarrow geopandas

### Step 4: Prepare the Taxi Data

Run: 
python prepare_taxi_data.py

This script loads the original taxi Parquet file, selects the needed columns, removes invalid rows, creates time fields, and saves a smaller CSV subset.

Expected output:

Rows: 150000
File size: about 12.8 MB
Saved file: nyc_taxi_subset.csv

### Step 5: Add Geo Fields

Run:
python add_geo_fields.py

This script joins the taxi data with the NYC taxi zone shapefile using PULocationID and DOLocationID. It creates pickup and dropoff coordinate fields for the Kibana map.

Expected output:

Rows: 100000
File size: about 28.2 MB
Saved file: nyc_taxi_subset_with_geo.csv

### Step 6: Upload Data to Elasticsearch

In Kibana:

Go to Machine Learning.
Click Data Visualizer.
Upload nyc_taxi_subset.csv.
Create the index nyc_taxi.
Upload nyc_taxi_subset_with_geo.csv.
Create the index nyc_taxi_geo2.

For the geo file, open the Mappings tab and set these two fields as geo_point:

"pickup_location": {
  "type": "geo_point"
},
"dropoff_location": {
  "type": "geo_point"
}

### Step 7: Create Kibana Visualizations
Set the time range to:

March 1, 2026 → March 31, 2026

Create the following visualizations:

Trip Count by Pickup Hour
Chart type: Bar
Horizontal axis: pickup_hour
Vertical axis: Count of records
Average Fare by Pickup Hour
Chart type: Line
Horizontal axis: pickup_hour
Vertical axis: Average of fare_amount
Average Trip Distance by Pickup Hour
Chart type: Line
Horizontal axis: pickup_hour
Vertical axis: Average of trip_distance
Top Pickup Location IDs by Trip Count
Chart type: Bar
Horizontal axis: Top 10 values of PULocationID
Vertical axis: Count of records
Turn off the “Other” bucket if it appears.
Geo-Temporal Map of NYC Taxi Pickups
Go to Maps
Add a Documents layer
Data view: nyc_taxi_geo2
Geospatial field: pickup_location
Time range: March 2026

### Step 8: Create the Dashboard

Create a Kibana dashboard named:

NYC Taxi Analysis Dashboard
Add all saved visualizations to the dashboard.

Machine Learning Plan

The predictive analysis task is to predict taxi fare_amount.

Model type: Regression

Input features:

trip_distance
trip_duration_minutes
passenger_count
pickup_hour
pickup_day
PULocationID
DOLocationID
payment_type
pickup_borough
dropoff_borough

Expected strongest influencers:

Trip distance
Trip duration
