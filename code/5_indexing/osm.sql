CREATE INDEX IF NOT EXISTS idx_osm_geom ON osm USING GIST (osm_geom);
