ALTER TABLE osm ADD COLUMN osm_geom geometry(Point, 4326);
UPDATE osm
SET osm_geom = ST_SetSRID(ST_MakePoint(osm_longitude::double precision, osm_latitude::double precision), 4326);