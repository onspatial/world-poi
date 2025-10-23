-- This step assumes Nominatim were used to create the place table
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
\copy place_filtered TO 'osm.csv' CSV HEADER;
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
\copy osm FROM 'osm.csv' CSV HEADER;