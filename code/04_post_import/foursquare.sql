ALTER TABLE foursquare ADD COLUMN fsq_geom geometry(Point, 4326);
UPDATE foursquare
SET fsq_geom = ST_SetSRID(ST_MakePoint(fsq_longitude::double precision, fsq_latitude::double precision), 4326);