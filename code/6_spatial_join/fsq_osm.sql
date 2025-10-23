CREATE TABLE fsq_osm AS
SELECT f.*, o.*
FROM foursquare f
LEFT OUTER JOIN osm o
ON ST_DWithin(f.fsq_geom, o.osm_geom, 0.0005);

