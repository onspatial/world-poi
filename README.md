<img width="1509" height="716" alt="image" src="https://github.com/user-attachments/assets/0e8f4462-582f-4a4b-9b6a-fabaa50b07a9" />

# Download the Dataset:

To download the World-POI dataset, please visit our [OSF repository](https://osf.io/p96uf/files).

We filter the integrated **631 GB (295,176,261 rows)** dataset to provide multiple smaller versions of the dataset to cater to different use cases.

_Please note that we don't provide the full dataset due to its large size, but you can follow the instructions in this repository to reproduce the full dataset._

## Tabular Data:

| name                                                           | description                                              | Size   | #POIs      |
| -------------------------------------------------------------- | -------------------------------------------------------- | ------ | ---------- |
| [World-POI-levenshtein_0.5.csv](https://osf.io/p96uf/download) | Filtered dataset with Levenshtein similarity score > 0.5 | 8.4 GB | 7,789,246  |
| [World-POI-levenshtein_0.3.csv](https://osf.io/p96uf/download) | Filtered dataset with Levenshtein similarity score > 0.3 | 18 GB  | 16,146,764 |
| [World-POI-trigrams_0.5.csv](https://osf.io/p96uf/download)    | Filtered dataset with Trigram similarity score > 0.5     | 7.8 GB | 7,205,821  |
| [World-POI-trigrams_0.3.csv](https://osf.io/p96uf/download)    | Filtered dataset with Trigram similarity score > 0.3     | 13 GB  | 1,120,944  |

## Graph Data:

| name                                                                      | description                                                                    | Size   | #Edges      |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------ | ----------- |
| [World-POI-graph_10nn-levenshtein_0.5.csv](https://osf.io/p96uf/download) | Graph dataset with Levenshtein similarity score > 0.5 and 10 nearest neighbors | 5 GB   | 77,892,460  |
| [World-POI-graph_10nn-levenshtein_0.3.csv](https://osf.io/p96uf/download) | Graph dataset with Levenshtein similarity score > 0.3 and 10 nearest neighbors | 11 GB  | 161,467,640 |
| [World-POI-graph_10nn-trigrams_0.5.csv](https://osf.io/p96uf/download)    | Graph dataset with Trigram similarity score > 0.5 and 10 nearest neighbors     | 4.6 GB | 72,058,210  |
| [World-POI-graph_10nn-trigrams_0.3.csv](https://osf.io/p96uf/download)    | Graph dataset with Trigram similarity score > 0.3 and 10 nearest neighbors     | 7.2 GB | 112,094,410 |

# Reproducing Results from the Paper

This document outlines the steps required to reproduce the results presented in our paper:  
**_"World-POI: Global Point-of-Interest Data Enriched from FourSquare and OpenStreetMap as Tabular and Graph Data"_**.

All source code, sample datasets, and processing scripts used in the study are provided in this repository. By following the instructions below, you will be able to recreate the full data processing pipeline, perform enrichment using OpenStreetMap (OSM) data, and generate both structured and graph-based representations of the final dataset. This includes environment setup, data acquisition, preprocessing, and evaluation scripts.

# Environment Setup

The experiments were conducted on a machine running **Ubuntu 22.04.1** with the following specifications:

- **Memory**: 256 GB RAM
- **Processor**: Intel(R) Xeon(R) CPU E5-2643 v2 @ 3.50GHz (24 cores)
- **Python version**: 3.10.12
- **PostgreSQL version**: 17.4
- **PostGIS version**: 3.5.2
- **Nominatim version**: 5.1.0

We recommend using `pipenv` to manage the Python environment and ensure reproducibility. To install all dependencies and activate the environment, run:

```bash
pipenv install
pipenv shell
```

If you prefer not to use pipenv, you can install the required packages manually using pip:

```bash
pip install pandas==2.2.3 \
            pyarrow==20.0.0 \
            numpy==2.2.6 \
            DateTime==5.5 \
            geopandas==1.0.1 \
            requests==2.32.3
```

Make sure your environment matches these versions to avoid compatibility issues during data processing or analysis.

# Data Preparation

## Download the Data

### Foursquare Data

To obtain the Foursquare POI data, run the script [**foursquare.py**](code/datacollection/foursquare.py). This script downloads the complete dataset and saves it in the `data/` directory as a single file named `foursquare.csv`. We drop the geometry column (`geom`) from the dataset to avoid datatype issues during import into PostgreSQL and name the cleaned file `foursquare_clean.csv`. This prevents binary-string errors during import. Geometries are later reconstructed using the latitude and longitude fields.

```bash
python code/datacollection/foursquare.py
```

**Memory Note:** The script concatenates large amounts of data and may consume substantial memory. If you encounter performance issues, we recommend using the provided Bash script [concat.sh](code/datacollection/concat.sh), which performs more memory-efficient concatenation:

```bash
bash code/datacollection/concat.sh
```

### OpenStreetMap (OSM) Data:

To enrich the Foursquare data with geographic features, we use the global OSM dataset in PBF format. The data can be downloaded from the [Planet OSM](https://planet.openstreetmap.org/) archive. The full [file](https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf) is approximately 80 GB, so ensure sufficient disk space before proceeding.

We downloaded using the following command:

```bash
wget https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf
```

Save the file in a designated directory (e.g., `osm/data`) for subsequent processing.

## Import Data into PostgreSQL

We use PostgreSQL to store and manage the Foursquare and OSM datasets. The data is imported into a new database named **`fsq-osm`**, which contains two main tables: `foursquare` and `osm`.

### Step 1: Create the Database

Run the following command to create a new PostgreSQL database:

```bash
createdb fsq-osm
```

### Step 2: Connect to the Database

Use the `psql` CLI tool to connect to the newly created database:

```bash
psql -d fsq-osm
```

---

Once connected, you can execute SQL commands to create the necessary schema and import data. Detailed SQL import commands and schema definitions are provided in the import.sql file in the repository.

We store the data in a new database called `fsq-osm`, which will have two tables: `foursquare` and `osm`.

To create a new database, you can use the following command:

```bash
createdb fsq-osm
```

Then, connect to the database using the following command:

### Foursquare Data:

To import the [downloaded](code/datacollection/foursquare.sql) Foursquare data into PostgreSQL, we first create the `foursquare` table in the `fsq-osm` database. You can use the following SQL command to create the table:

```sql
CREATE TABLE foursquare (
      fsq_place_id        text,
      fsq_name            text,
      fsq_latitude        DOUBLE PRECISION,
      fsq_longitude       DOUBLE PRECISION,
      fsq_address         text,
      fsq_locality        text,
      fsq_region          text,
      fsq_postcode        text,
      fsq_admin_region    text,
      fsq_post_town       text,
      fsq_po_box          text,
      fsq_country         text,
      fsq_date_created    text,
      fsq_date_refreshed  text,
      fsq_date_closed     text,
      fsq_tel             text,
      fsq_website         text,
      fsq_email           text,
      fsq_facebook_id     text,
      fsq_instagram       text,
      fsq_twitter         text,
      fsq_category_ids    text,
      fsq_category_labels text,
      fsq_placemaker_url  text,
      fsq_unresolved_flags text,
      fsq_bbox            text
);
```

Then we can import the data from the `foursquare_clean.csv` file into the `foursquare` table using the following command:

```sql
\copy foursquare FROM 'foursquare_clean.csv' WITH ( FORMAT csv, HEADER, DELIMITER ',', QUOTE '"', ESCAPE '"', NULL '' );
```

### OSM Data:

First the downloaded OSM data is converted into PostgreSQL. To convert the OSM data into PostgreSQL, we use [`nominatim`](https://nominatim.org/) tool.

You can install it using the following command:

```bash
pip install nominatim-db nominatim-api
```

Since we are importing the entire planet data, it is recommended to use a flatnode file to speed up the import process.

```bash
NOMINATIM_FLATNODE_FILE="/path/to/flatnode.file"
```

Then, you can use the following command to import the OSM data into PostgreSQL:

```bash
PGPASSWORD=your_psql_user_password nominatim import --osm-file ./planet-latest.osm.pbf
```

For the most recent version and detailed instructions, please refer to the official documentation on the [Nominatim website](https://nominatim.org)

After importing, you need to connect to the database:

```bash
psql -d nominatim
```

we only use the places that have address and name from the OSM data:

```sql
CREATE TABLE place_filtered AS
SELECT
    p.osm_id AS osm_id,
    p.class AS osm_class,
    p.type AS osm_type,
    p.name AS osm_name,
    p.address AS osm_address,
    p.extratags AS osm_extratags,
    p.geometry AS osm_geometry,
    ST_Y(ST_Centroid(p.geometry)) AS osm_latitude,
    ST_X(ST_Centroid(p.geometry)) AS osm_longitude
FROM place p
WHERE class <> 'highway' AND name IS NOT NULL;

```

Then we export the data to a CSV file using the following command:

```sql
\copy place_filtered TO 'osm.csv' CSV HEADER
```

Next, disconnect from the `nominatim` database and connect to the `fsq-osm` database. Then, import the osm data into the fsq-osm database as follows.

```sql
CREATE TABLE osm (
  osm_id BIGINT,
  osm_class TEXT,
  osm_type TEXT,
  osm_name TEXT,
  osm_address TEXT,
  osm_extratags TEXT,
  osm_geometry GEOMETRY,
  osm_latitude DOUBLE PRECISION,
  osm_longitude DOUBLE PRECISION
);
```

Then we can import the data from the `osm.csv` file into the `osm` table using the following command:

```sql
\copy osm FROM 'osm.csv' CSV HEADER
```

Now we have the `foursquare` and `osm` tables in the `fsq-osm` database.

# Preprocessing the Data

After importing the data into PostgreSQL, we need to process the data to prepare it for analysis. The following steps outline how to process the Foursquare and OSM data.

## Adding Geometry Columns:

We use PostGIS to calculate the geometry from the latitude and longitude values in the `foursquare` and `osm` tables.
For the `foursquare` table, we add a new column called `fsq_geom` to store the geometry. The `fsq_geom` column is of type `geometry(Point, 4326)`, which is a point geometry in the WGS 84 coordinate system (EPSG:4326).
To add the `fsq_geom` column, we first need to ensure that the PostGIS extension is enabled in the database. We also use other extensions for the future steps. You can enable them using the following command:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
```

Next, we can add the `fsq_geom` column to the `foursquare` table and calculate the geometry using the latitude and longitude values. The latitude and longitude columns in the `foursquare` table are named `latitude` and `longitude`, respectively.

We can add the `fsq_geom` column to the `foursquare` table using the following SQL command:

```sql
ALTER TABLE foursquare ADD COLUMN fsq_geom geometry(Point, 4326);
UPDATE foursquare
SET fsq_geom = ST_SetSRID(ST_MakePoint(fsq_longitude::double precision, fsq_latitude::double precision), 4326);
```

For the `osm` table, we use the same command to add the `osm_geom` column. Please note that the `latitude` and `longitude` columns in the `osm` table are named `osm_latitude` and `osm_longitude`, respectively.

```sql
ALTER TABLE osm ADD COLUMN osm_geom geometry(Point, 4326);
UPDATE osm
SET osm_geom = ST_SetSRID(ST_MakePoint(osm_longitude::double precision, osm_latitude::double precision), 4326);
```

## Adding Indexes:

To speed up the queries, we add indexes to the `geom` column in both tables. You can use the following SQL commands to add the indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_fsq_geom ON foursquare USING GIST (fsq_geom);
CREATE INDEX IF NOT EXISTS idx_osm_geom ON osm USING GIST (osm_geom);
```

## Joining Foursquare and OSM Data:

To join the Foursquare and OSM data, we can use the ST_DWithin function to identify points that fall within a specified distance of each other. A threshold of 0.0005 degrees (approximately 55 meters) can be used to treat two points as the same location. Using a larger distance will produce a much larger joined table.

```sql
CREATE TABLE fsq_osm AS
SELECT f.*, o.*
FROM foursquare f
LEFT OUTER JOIN osm o
ON ST_DWithin(f.fsq_geom, o.osm_geom, 0.0005);
```

As a case study, we can use the following SQL command to select only the data for the United States. This command creates a new table called fsq_osm_usa that contains the joined records from both datasets restricted to the U.S. The ST_DWithin function ensures that the geometries of the Foursquare and OSM points are within 0.001 degrees (approximately 100 meters) of each other.

```sql
CREATE TABLE fsq_osm_usa AS
SELECT f.*, o.*
FROM foursquare f
LEFT OUTER JOIN osm o
ON ST_DWithin(f.fsq_geom, o.osm_geom, 0.001)
WHERE f.fsq_country='US';
```

## Data Type Conversion

In the fsq_osm table, osm_name and osm_extratags are stored as text that contains hstore-formatted strings. To compare Foursquare and OSM names, extract the OSM name into a plain TEXT column while leaving the address as hstore-formatted text to save space.

```sql
ALTER TABLE fsq_osm
ALTER COLUMN osm_name TYPE text
USING (osm_name::hstore -> 'name');
```

# Calculating the Similarity:

To calculate the similarity between the Foursquare and OSM data, we use two approaches. The distance between longitude and latitude of foursquare and osm as a separate column in the data. We also provide a similarity score between the name of the place in foursquare and osm.

Using the name_similarity_score, you can see how similar the names are and using coordinate distance you can see how close the location in spatially.

```sql
ALTER TABLE fsq_osm ADD COLUMN fsq_osm_name_similarity_score DOUBLE PRECISION;
ALTER TABLE fsq_osm ADD COLUMN fsq_osm_distance DOUBLE PRECISION;
```

```sql
UPDATE fsq_osm
SET fsq_osm_distance = ST_Distance(fsq_geom, osm_geom);
```

```sql
UPDATE fsq_osm
SET fsq_osm_name_similarity_score = GREATEST(similarity(LOWER(fsq_name), LOWER(osm_name)), 0.0);
```

```sql
CREATE OR REPLACE FUNCTION levenshtein_similarity(a text, b text)
RETURNS double precision
LANGUAGE sql
IMMUTABLE
AS $$
  SELECT CASE
    WHEN a IS NULL OR b IS NULL THEN NULL
    WHEN length(a) = 0 AND length(b) = 0 THEN 1.0
    ELSE 1.0 - levenshtein(a, b)::float / GREATEST(length(a), length(b))
  END;
$$;
```

```sql
ALTER TABLE fsq_osm
ADD COLUMN fsq_osm_name_similarity_score_lev double precision;

UPDATE fsq_osm
SET fsq_osm_name_similarity_score_lev =
    levenshtein_similarity(fsq_name, osm_name);
```

# Exporting the Final Dataset

To export the final dataset, we can use the `\copy` command to export the `fsq_osm` table to a CSV file. You can use the following SQL command:

```sql
\copy fsq_osm TO 'fsq_osm.csv' CSV HEADER
```

This command exports the `fsq_osm` table to a CSV file named `fsq_osm.csv` in the current directory. The `CSV HEADER` option ensures that the column names are included in the first row of the CSV file.

# Filter dataset based on similarity score and distance

To filter the dataset based on similarity score, you can use the following SQL command:

```sql
CREATE TABLE fsq_osm_filtered_5 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score > 0.5;
```

```
CREATE TABLE fsq_osm_filtered_5_lev AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.5;
```

This command creates a new table called `fsq_osm_filtered_5` that contains only the rows from the `fsq_osm` table where the `name_similarity_score` is greater than 0.5.

```sql
CREATE TABLE fsq_osm_filtered_usa_3 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score > 0.3 AND fsq_country='US' ;
```

This command creates a new table called `fsq_osm_filtered_usa_3` that contains only the rows from the `fsq_osm` table where the `name_similarity_score` is greater than 0.3 and the country is 'US'.

T export it to csv:

```sql
\copy fsq_osm_filtered_5 TO 'fsq_osm_filtered_5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
```

# Generate a Graph from the data

```sql
-- 1) Ensure a spatial index (run once)
CREATE INDEX IF NOT EXISTS fsq_osm_filtered_5_gix ON fsq_osm_filtered_5 USING GIST (fsq_geom);

-- 2) Build the (source, destination, distance_m) table
CREATE TABLE fsq_graph_10 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM fsq_osm_filtered_5 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM fsq_osm_filtered_5 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  -- K-NN using geometry index; fast and exact for ordering
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;

-- 3) Index the result for fast lookups
CREATE INDEX ON fsq_nn10 (fsq_place_id_source);
CREATE INDEX ON fsq_nn10 (fsq_place_id_destination);
ANALYZE fsq_nn10;
```

To make the lookup table for visualization:

```sql
CREATE TABLE fsq_osm_lookup AS
SELECT fsq_place_id, fsq_name, fsq_latitude, fsq_longitude, fsq_category_labels
FROM fsq_osm_filtered_5;
```

```sql

CREATE TABLE fsq_graph_10_visualization AS
SELECT
s.fsq_place_id AS fsq_place_id_source,
s.fsq_latitude AS fsq_latitude_source,
s.fsq_longitude AS fsq_longitude_source,
d.fsq_place_id AS fsq_place_id_destination,
d.fsq_latitude AS fsq_latitude_destination,
d.fsq_longitude AS fsq_longitude_destination,
ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM fsq_osm_filtered_5 AS s
JOIN LATERAL (
SELECT fsq_place_id,fsq_latitude,fsq_longitude, fsq_geom
FROM fsq_osm_filtered_5 AS d
WHERE d.fsq_place_id <> s.fsq_place_id
-- K-NN using geometry index; fast and exact for ordering
ORDER BY s.fsq_geom <-> d.fsq_geom
LIMIT 10
) AS d ON TRUE;

-- 3) Index the result for fast lookups
CREATE INDEX ON fsq_nn10 (fsq_place_id_source);
CREATE INDEX ON fsq_nn10 (fsq_place_id_destination);
ANALYZE fsq_nn10;

```
