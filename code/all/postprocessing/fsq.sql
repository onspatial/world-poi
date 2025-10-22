ALTER TABLE foursquare ADD COLUMN geom geometry(Point, 4326);
UPDATE foursquareSET geom = ST_SetSRID(
                  ST_MakePoint(longitude::double precision, latitude::double precision),              4326          )WHERE     latitude ~ '^\-?\d+(\.\d+)?$' AND     longitude ~ '^\-?\d+(\.\d+)?$';