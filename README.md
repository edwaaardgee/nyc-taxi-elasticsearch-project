# NYC Taxi Trip Data Analysis Using Elasticsearch and Kibana

## Project Overview

This project analyzes NYC Yellow Taxi Trip Records using Elasticsearch, Kibana, and Python. The dataset was downloaded from the New York City Taxi and Limousine Commission. We cleaned and sampled the data, uploaded it into Elasticsearch, created Kibana visualizations, and built a geo-temporal map of taxi pickups.

The goal of this project is to show how real-world transportation data can be processed, stored, visualized, and prepared for predictive analysis using Elasticsearch and Kibana.

## Data Source

NYC TLC Trip Record Data:  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Dataset used:

```text
Yellow Taxi Trip Records, March 2026
```

Additional geographic data used:

```text
NYC Taxi Zone Shapefile
```

The taxi zone shapefile was used to convert pickup and dropoff location IDs into approximate geographic coordinates for the Kibana map.

## Platform Specs

- Platform: Elastic Cloud / Kibana
- Operating System: Windows 11
- Python Version: 3.13.13
- Libraries: pandas, pyarrow, geopandas
- Original dataset rows: 3,952,451
- Cleaned subset: 150,000 rows, 12.8 MB
- Geo subset: 100,000 rows, 28.2 MB
- Elasticsearch indexes: `nyc_taxi`, `nyc_taxi_geo2`

## Repository Files

This repository includes:

```text
README.md
prepare_taxi_data.py
add_geo_fields.py
```

The Python files are used for data preparation:

- `prepare_taxi_data.py` cleans and samples the original NYC taxi dataset.
- `add_geo_fields.py` joins the taxi data with the NYC taxi zone shapefile and creates geo-point fields for Kibana Maps.

## Important File Setup

Before running the Python scripts, place these files in the same folder as the scripts:

- `yellow_tripdata_2026-03.parquet`
- The extracted `taxi_zones` folder

Your project folder should look like this:

```text
nyc-taxi-elasticsearch-project-main/
├── README.md
├── prepare_taxi_data.py
├── add_geo_fields.py
├── yellow_tripdata_2026-03.parquet
└── taxi_zones/
    ├── taxi_zones.shp
    ├── taxi_zones.dbf
    ├── taxi_zones.shx
    └── other shapefile files
```

The taxi zone shapefile must stay inside a folder named:

```text
taxi_zones
```

## How to Reproduce the Project

### Step 1: Download the NYC Taxi Dataset

Go to the NYC TLC Trip Record Data page:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Download the March 2026 Yellow Taxi Trip Records file.

Expected file name:

```text
yellow_tripdata_2026-03.parquet
```

Place this file in the same folder as the Python scripts.

## Step 2: Download the Taxi Zone Shapefile

On the same NYC TLC page, find the Taxi Zone Maps / Lookup Tables section.

Download the Taxi Zone Shapefile.

Extract the ZIP file and place the extracted folder inside the project folder.

Expected shapefile path:

```text
taxi_zones/taxi_zones.shp
```

## Step 3: Install Python Libraries

Open Command Prompt or PowerShell in the project folder and run:

```bash
python -m pip install pandas pyarrow geopandas
```

These libraries are used for:

- `pandas`: loading, cleaning, and sampling the taxi dataset
- `pyarrow`: reading the Parquet file format
- `geopandas`: reading the taxi zone shapefile and creating location coordinates

## Step 4: Prepare the Taxi Data

Run the first Python script:

```bash
python prepare_taxi_data.py
```

This script does the following:

1. Loads the original NYC Yellow Taxi Parquet file.
2. Selects the columns needed for the project.
3. Removes missing and invalid rows.
4. Creates new time-based fields:
   - `pickup_hour`
   - `pickup_day`
   - `trip_duration_minutes`
5. Samples the data into a smaller CSV file for Elasticsearch.
6. Saves the cleaned file as `nyc_taxi_subset.csv`.

Expected output:

```text
Rows: 150000
File size: 12.80 MB
Saved file: nyc_taxi_subset.csv
```

After running this step, the project folder should include:

```text
nyc_taxi_subset.csv
```

## Step 5: Add Geo Fields for the Map

Run the second Python script:

```bash
python add_geo_fields.py
```

This script does the following:

1. Loads the cleaned taxi CSV file.
2. Loads the NYC taxi zone shapefile.
3. Matches `PULocationID` and `DOLocationID` with taxi zone information.
4. Adds pickup and dropoff borough and zone names.
5. Creates approximate latitude and longitude coordinates using taxi zone centroids.
6. Creates geo-point fields for Kibana Maps:
   - `pickup_location`
   - `dropoff_location`
7. Saves the geo-enhanced CSV file as `nyc_taxi_subset_with_geo.csv`.

Expected output:

```text
Rows: 100000
File size: 28.22 MB
Saved file: nyc_taxi_subset_with_geo.csv
```

After running this step, the project folder should include:

```text
nyc_taxi_subset.csv
nyc_taxi_subset_with_geo.csv
```

## Step 6: Upload the Cleaned Dataset to Elasticsearch

Open Kibana.

Go to:

```text
Machine Learning → Data Visualizer → Upload file
```

Upload:

```text
nyc_taxi_subset.csv
```

Create a new index named:

```text
nyc_taxi
```

Click Import.

Expected result:

Kibana should show that the index was created, the file was uploaded, and the documents are searchable.

## Step 7: Upload the Geo Dataset to Elasticsearch

Go back to:

```text
Machine Learning → Data Visualizer → Upload file
```

Upload:

```text
nyc_taxi_subset_with_geo.csv
```

Create a new index named:

```text
nyc_taxi_geo2
```

Before importing, open the Mappings tab.

Make sure these fields are mapped as `geo_point`:

```json
"pickup_location": {
  "type": "geo_point"
},
"dropoff_location": {
  "type": "geo_point"
}
```

Then click Import.

Expected result:

The index `nyc_taxi_geo2` should be created with `pickup_location` and `dropoff_location` available as geospatial fields for Kibana Maps.

## Step 8: Set the Kibana Time Range

In Kibana, set the time range to:

```text
March 1, 2026 → March 31, 2026
```

This time range is important because the dataset uses March 2026 taxi trip records.

## Step 9: Create Kibana Visualizations

Create the following visualizations in Kibana Lens.

### Visualization 1: Trip Count by Pickup Hour

Chart type:

```text
Bar chart
```

Configuration:

- Horizontal axis: `pickup_hour`
- Vertical axis: Count of records

Save as:

```text
Trip Count by Pickup Hour
```

Purpose:

This chart shows how taxi trip volume changes throughout the day.

### Visualization 2: Average Fare by Pickup Hour

Chart type:

```text
Line chart
```

Configuration:

- Horizontal axis: `pickup_hour`
- Vertical axis: Average of `fare_amount`

Save as:

```text
Average Fare by Pickup Hour
```

Purpose:

This chart shows how the average taxi fare changes by hour of day.

### Visualization 3: Average Trip Distance by Pickup Hour

Chart type:

```text
Line chart
```

Configuration:

- Horizontal axis: `pickup_hour`
- Vertical axis: Average of `trip_distance`

Save as:

```text
Average Trip Distance by Pickup Hour
```

Purpose:

This chart shows whether trips are shorter or longer depending on the pickup hour.

### Visualization 4: Top Pickup Location IDs by Trip Count

Chart type:

```text
Bar chart
```

Configuration:

- Horizontal axis: Top 10 values of `PULocationID`
- Vertical axis: Count of records

Turn off the “Other” bucket if it appears.

Save as:

```text
Top Pickup Location IDs by Trip Count
```

Purpose:

This chart shows which pickup location IDs had the highest taxi activity.

## Step 10: Create the Geo-Temporal Map

Go to:

```text
Maps → Create map → Add layer
```

Choose:

```text
Documents
```

Use this data view:

```text
nyc_taxi_geo2
```

Choose this geospatial field:

```text
pickup_location
```

Set the time range to:

```text
March 2026
```

Save the map as:

```text
Geo-Temporal Map of NYC Taxi Pickups
```

Purpose:

This map shows taxi pickup activity across New York City during March 2026. The map uses pickup zone centroid coordinates created from the NYC taxi zone shapefile.

## Step 11: Create the Dashboard

Create a Kibana dashboard named:

```text
NYC Taxi Analysis Dashboard
```

Add all saved visualizations:

1. Trip Count by Pickup Hour
2. Average Fare by Pickup Hour
3. Average Trip Distance by Pickup Hour
4. Top Pickup Location IDs by Trip Count
5. Geo-Temporal Map of NYC Taxi Pickups

The dashboard summarizes taxi activity by time, fare, distance, location ID, and geographic pickup patterns.

## Machine Learning Plan

The predictive analysis task is to predict taxi `fare_amount`.

Model type:

```text
Regression
```

Target field:

```text
fare_amount
```

Input features:

- `trip_distance`
- `trip_duration_minutes`
- `passenger_count`
- `pickup_hour`
- `pickup_day`
- `PULocationID`
- `DOLocationID`
- `payment_type`
- `pickup_borough`
- `dropoff_borough`

Expected strongest influencers:

- Trip distance
- Trip duration
- Pickup and dropoff location

Reason for using regression:

Fare amount is a continuous numeric value, so regression is appropriate for predicting the expected fare based on trip features.

## Project Workflow

```text
NYC TLC Dataset
→ Python Data Cleaning
→ Sampled CSV Dataset
→ Taxi Zone Shapefile Join
→ Geo Fields Added
→ Elasticsearch Indexes
→ Kibana Visualizations
→ Geo-Temporal Map
→ Machine Learning Fare Prediction Plan
```

## Reproducibility Test

The project workflow was tested from a clean folder. The scripts successfully recreated both CSV files:

```text
python prepare_taxi_data.py
```

Output:

```text
Rows: 150000
File size: 12.80 MB
Saved file: nyc_taxi_subset.csv
```

Then:

```text
python add_geo_fields.py
```

Output:

```text
Rows: 100000
File size: 28.22 MB
Saved file: nyc_taxi_subset_with_geo.csv
```

This confirms that the GitHub instructions can be followed to recreate the project files.

## References

1. NYC Taxi & Limousine Commission Trip Record Data:  
   https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

2. Elasticsearch Documentation:  
   https://www.elastic.co/docs

3. Kibana Documentation:  
   https://www.elastic.co/docs
