# NYC Taxi Trip Data Analysis Using Elasticsearch, Kibana, and Machine Learning

## Project Overview

This project analyzes NYC Yellow Taxi trip data using Python, Elasticsearch, Kibana, and Kibana Machine Learning. The goal of the project is to clean and prepare a real-world transportation dataset, upload it into Elasticsearch, build visualizations in Kibana, create a geo-temporal map, and train a machine learning regression model to predict taxi fare amount.

The project uses the March 2026 NYC Yellow Taxi Trip Records dataset from the NYC Taxi and Limousine Commission. Python was used to clean the original Parquet file, create smaller CSV subsets, add time-based fields, and add geographic fields using the NYC Taxi Zone Shapefile. Elasticsearch was used to store and index the data, while Kibana was used for dashboards, maps, and machine learning analysis.

## Full Tutorial

The complete step-by-step tutorial is included separately as:

`CIS3200_Group6_Term_Project_Tutorial.pdf`

The tutorial explains how to download the dataset, prepare the data, upload the files into Elasticsearch, create Kibana visualizations, build the geo-temporal map, and run the machine learning regression model.

This README gives a project overview, workflow summary, key results, and reproduction outline.

## Project Goals

- Download and prepare NYC Yellow Taxi trip data
- Clean and sample the original dataset using Python
- Add pickup and drop-off geographic fields using the NYC Taxi Zone Shapefile
- Upload cleaned datasets into Elasticsearch
- Build Kibana visualizations and a dashboard
- Create a geo-temporal pickup map using Kibana Maps
- Build a machine learning regression model to predict taxi fare amount
- Evaluate the model using R², MSE, RMSE, and feature importance/influencers

## Tools and Technologies Used

- Python
- pandas
- pyarrow
- GeoPandas
- Elasticsearch
- Kibana
- Kibana Data Visualizer
- Kibana Lens
- Kibana Maps
- Kibana Machine Learning Data Frame Analytics
- Elastic Cloud
- NYC Taxi and Limousine Commission Dataset

## Dataset

The dataset used in this project is the NYC Yellow Taxi Trip Records dataset for March 2026.

Dataset source:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Files used:

- `yellow_tripdata_2026-03.parquet`
- NYC Taxi Zone Shapefile

Dataset details:

| Item | Value |
|---|---|
| Dataset | NYC Yellow Taxi Trip Records |
| Month | March 2026 |
| Original Rows | 3,952,451 |
| Original Columns | 20 |
| Original File Size | Approximately 64.8 MB |
| Cleaned CSV Subset | 150,000 rows |
| Cleaned CSV Size | Approximately 12.8 MB |
| Geo-Enhanced CSV Subset | 100,000 rows |
| Geo-Enhanced CSV Size | Approximately 28.2 MB |

## Hardware and Environment

The project was completed using a personal Windows computer for local data preparation and Elastic Cloud/Kibana for indexing, visualization, and machine learning.

| Item | Specification |
|---|---|
| Operating System | Windows 11 |
| Processor | 12th Gen Intel(R) Core(TM) i7-12700K |
| Memory | 32 GB RAM |
| System Type | 64-bit operating system |
| Python Version | Python 3.13.13 |
| Cloud Platform | Elastic Cloud / Kibana |
| Search Engine | Elasticsearch |

## Project Workflow

The project follows this general process:

```text
Download NYC Taxi Data
↓
Download Taxi Zone Shapefile
↓
Clean and Sample Data with Python
↓
Create Time-Based Fields
↓
Join Taxi Data with Taxi Zone Shapefile
↓
Create Geo Fields for Kibana Maps
↓
Upload CSV Files into Elasticsearch
↓
Create Kibana Visualizations
↓
Build Kibana Dashboard
↓
Create Geo-Temporal Map
↓
Train Machine Learning Regression Model
↓
Evaluate Accuracy and Feature Importance
```

## Elasticsearch Indexes Created

The following Elasticsearch indexes were created:

| Index Name | Purpose |
|---|---|
| `nyc_taxi` | Stores the cleaned taxi trip dataset |
| `nyc_taxi_geo` | Stores the geo-enhanced taxi dataset |
| `nyc_taxi_fare_prediction` | Stores the machine learning regression prediction results |

## Python Data Preparation

The first Python script cleans the original taxi dataset and creates a smaller CSV file for Elasticsearch.

Main cleaning steps:

- Load the original Parquet file
- Keep only the columns needed for analysis
- Remove missing values
- Remove invalid trips with zero or negative distance
- Remove invalid fare and total amount records
- Create `pickup_hour`
- Create `pickup_day`
- Create `trip_duration_minutes`
- Remove unrealistic trip durations
- Save a cleaned CSV subset

Output file:

`nyc_taxi_subset.csv`

## Geo-Enhanced Dataset

The second Python script adds geographic fields to the taxi data by using the NYC Taxi Zone Shapefile.

Main geo-processing steps:

- Load `nyc_taxi_subset.csv`
- Load the NYC Taxi Zone Shapefile
- Convert taxi zone polygons into centroid points
- Join pickup location IDs with taxi zone data
- Join drop-off location IDs with taxi zone data
- Add pickup and drop-off latitude/longitude
- Add pickup and drop-off zone names
- Add pickup and drop-off borough names
- Create `pickup_location` and `dropoff_location` geo-point fields
- Save the geo-enhanced CSV file

Output file:

`nyc_taxi_subset_with_geo.csv`

## Kibana Visualizations

The project includes four main Kibana Lens visualizations.

### 1. Trip Count by Pickup Hour

This visualization shows taxi demand by hour of the day.

**Insight:** Taxi demand increases after the morning hours and peaks later in the day.

### 2. Average Fare by Pickup Hour

This visualization shows how average taxi fare changes by pickup hour.

**Insight:** Average fare spikes around early morning hours.

### 3. Average Trip Distance by Pickup Hour

This visualization shows how average taxi trip distance changes by pickup hour.

**Insight:** Early morning trips show the longest average distance.

### 4. Top Pickup Location IDs by Trip Count

This visualization shows which pickup location IDs had the highest taxi activity.

**Insight:** Pickup Location IDs such as 237, 132, 161, and 236 showed high pickup activity.

## Geo-Temporal Map

A Kibana Maps visualization was created using the geo-enhanced dataset.

Map settings:

| Setting | Value |
|---|---|
| Data View | `nyc_taxi_geo` |
| Geo Field | `pickup_location` |
| Layer Type | Clusters |
| Time Range | March 1, 2026 to March 31, 2026 |

**Map insight:** Pickup activity was concentrated around Manhattan, Queens, Brooklyn, and airport-related zones.

## Machine Learning Regression Model

A Kibana Machine Learning Data Frame Analytics regression job was created to predict taxi fare amount.

Model settings:

| Setting | Value |
|---|---|
| Job Type | Regression |
| Source Data View | `nyc_taxi_geo` |
| Target Field | `fare_amount` |
| Training Percent | 80% |
| Destination Index | `nyc_taxi_fare_prediction` |
| Prediction Field | `fare_amount_prediction` |
| Top Feature Importance Values | 10 |

The `total_amount` field was excluded from the model because it is too closely related to `fare_amount` and could make the prediction artificially easy.

## Machine Learning Results

The regression model produced the following results:

| Metric | Value |
|---|---|
| Training Records | 80,000 |
| Testing Records | 20,000 |
| Testing R² Score | 0.95 |
| Testing Mean Squared Error | 13.6 |
| Training R² Score | 0.945 |
| Training Mean Squared Error | 15.2 |
| Testing RMSE | Approximately 3.69 |

The testing R² score of 0.95 means the model explained about 95% of the variation in taxi fare amount on the test data.

The RMSE of approximately 3.69 means the model’s fare predictions had an approximate error of $3.69 in RMSE terms.

## Feature Importance / Influencers

The most important influencers for predicting taxi fare amount were:

| Feature | Role in Model |
|---|---|
| `trip_distance` | Strongest influencer; longer trips usually have higher fare |
| `trip_duration_minutes` | Second strongest influencer; longer trip duration affects fare prediction |
| `pickup_zone` | Pickup area influences fare patterns |
| `dropoff_zone` | Drop-off area influences fare patterns |
| `pickup_borough` | Borough location affects fare prediction |
| `pickup_longitude` | Helps represent pickup geography |
| `pickup_latitude` | Helps represent pickup geography |
| `dropoff_longitude` | Helps represent drop-off geography |
| `dropoff_latitude` | Helps represent drop-off geography |
| `dropoff_borough` | Borough location affects fare prediction |

The results show that taxi fare is strongly related to trip distance and trip duration. Location-based fields also helped the model because different taxi zones and boroughs can have different fare patterns.

## How to Reproduce This Project

For the complete step-by-step instructions, use the full tutorial file included in this repository:

`CIS3200_Group6_Term_Project_Tutorial.pdf`

A shorter reproduction summary is included below.

### 1. Download the Dataset

Download the March 2026 Yellow Taxi Trip Records Parquet file from:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Expected file name:

`yellow_tripdata_2026-03.parquet`

### 2. Download the Taxi Zone Shapefile

Download the NYC Taxi Zone Shapefile from the same NYC TLC page and extract it into the project folder.

Expected folder structure:

```text
project-folder/
│
├── yellow_tripdata_2026-03.parquet
├── taxi_zones/
│   ├── taxi_zones.shp
│   ├── taxi_zones.dbf
│   ├── taxi_zones.shx
│   ├── taxi_zones.prj
│   └── other shapefile files
```

### 3. Install Python Libraries

Run:

```bash
python -m pip install pandas pyarrow geopandas
```

### 4. Prepare the Taxi Data

Run the data preparation code from this repository to create:

`nyc_taxi_subset.csv`

This script cleans the original Parquet dataset and creates a smaller CSV subset for Elasticsearch.

### 5. Add Geo Fields

Run the geo-enhancement code from this repository to create:

`nyc_taxi_subset_with_geo.csv`

This script joins the taxi trip data with the NYC Taxi Zone Shapefile and creates geographic fields for Kibana Maps.

### 6. Upload Files to Elasticsearch

Upload `nyc_taxi_subset.csv` into Elasticsearch as:

`nyc_taxi`

Upload `nyc_taxi_subset_with_geo.csv` into Elasticsearch as:

`nyc_taxi_geo`

Make sure the following fields are mapped as `geo_point`:

- `pickup_location`
- `dropoff_location`

### 7. Build Kibana Visualizations

Create the following visualizations in Kibana Lens:

- Trip Count by Pickup Hour
- Average Fare by Pickup Hour
- Average Trip Distance by Pickup Hour
- Top Pickup Location IDs by Trip Count

### 8. Build Kibana Map

Create a Kibana Maps cluster layer using:

```text
Data view: nyc_taxi_geo
Geo field: pickup_location
Layer type: Clusters
```

### 9. Build Machine Learning Regression Job

In Kibana, go to:

```text
Machine Learning → Data Frame Analytics → Create job
```

Use these settings:

```text
Job type: Regression
Source data view: nyc_taxi_geo
Target field: fare_amount
Training percent: 80%
Destination index: nyc_taxi_fare_prediction
Prediction field: fare_amount_prediction
Top feature importance values: 10
```

Do not include `total_amount` as an input feature because it is too closely related to `fare_amount`.

## Main Findings

- Taxi demand increases after the morning hours and peaks later in the day.
- Early morning trips have higher average fare and longer average trip distance.
- Pickup activity is concentrated around Manhattan, Queens, Brooklyn, and airport-related zones.
- The regression model predicted taxi fare amount with a testing R² score of 0.95.
- The testing RMSE was approximately $3.69.
- The strongest fare predictors were `trip_distance` and `trip_duration_minutes`.

## Project Files

Recommended repository files:

```text
README.md
prepare_taxi_data.py
add_geo_fields.py
CIS3200_Group6_Term_Project_Tutorial.pdf
```

The original dataset and generated CSV files may be too large for GitHub. If they are not included in the repository, they can be recreated by following the tutorial and running the Python scripts.

## Authors

- Ruben Chagollan
- Edward Gallegos
- Jordy Moreno
- Giovanni Clara

California State University, Los Angeles  
CIS 3200 – Data Processing and Analytics

## References

1. NYC Taxi & Limousine Commission. TLC Trip Record Data.  
   https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

2. NYC Taxi Zone Shapefile / Taxi Zone Maps and Lookup Tables.  
   https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

3. Elasticsearch Documentation.  
   https://www.elastic.co/docs

4. Kibana Documentation.  
   https://www.elastic.co/docs

5. pandas Documentation.  
   https://pandas.pydata.org/docs/

6. GeoPandas Documentation.  
   https://geopandas.org/
