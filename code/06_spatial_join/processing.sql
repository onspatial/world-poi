ALTER TABLE fsq_osm
ALTER COLUMN osm_name TYPE text
USING (osm_name::hstore -> 'name');

ALTER TABLE fsq_osm ADD COLUMN fsq_osm_name_similarity_score_trg DOUBLE PRECISION;
ALTER TABLE fsq_osm ADD COLUMN fsq_osm_name_similarity_score_lev DOUBLE PRECISION;
ALTER TABLE fsq_osm ADD COLUMN fsq_osm_distance DOUBLE PRECISION;

UPDATE fsq_osm
SET fsq_osm_distance = ST_Distance(fsq_geom, osm_geom);