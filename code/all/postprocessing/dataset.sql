-- ------------------------------------------------------------------------ World_POI_levenshtein_0.5.csv
CREATE TABLE World_POI_levenshtein_05 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.5;
CREATE INDEX IF NOT EXISTS World_POI_levenshtein_05_gix ON World_POI_levenshtein_05 USING GIST (fsq_geom);
\copy World_POI_levenshtein_05 TO 'World_POI_levenshtein_0.5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
-- World_POI_graph_10nn_levenshtein_0.5.csv
CREATE TABLE World_POI_graph_10nn_levenshtein_05 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM World_POI_levenshtein_05 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM World_POI_levenshtein_05 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;
\copy World_POI_graph_10nn_levenshtein_05 TO 'World_POI_graph_10nn_levenshtein_0.5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- ------------------------------------------------------------------------ World_POI_levenshtein_0.3.csv
CREATE TABLE World_POI_levenshtein_03 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.3;
CREATE INDEX IF NOT EXISTS World_POI_levenshtein_03_gix ON World_POI_levenshtein_03 USING GIST (fsq_geom);
\copy World_POI_levenshtein_03 TO 'World_POI_levenshtein_0.3.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
-- World-POI-graph_10nn-levenshtein_0.3.csv
CREATE TABLE World_POI_graph_10nn_levenshtein_03 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM World_POI_levenshtein_03 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM World_POI_levenshtein_03 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;
\copy World_POI_graph_10nn_levenshtein_03 TO 'World_POI_graph_10nn_levenshtein_0.3.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);


-- ------------------------------------------------------------------------ World-POI-trigrams_0.5.csv
CREATE TABLE World_POI_trigrams_05 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_trg > 0.5;
CREATE INDEX IF NOT EXISTS World_POI_trigrams_05_gix ON World_POI_trigrams_05 USING GIST (fsq_geom);
\copy World_POI_trigrams_05 TO 'World_POI_trigrams_0.5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
-- World-POI-graph_10nn-trigrams_0.5.csv
CREATE TABLE World_POI_graph_10nn_trigrams_05 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM World_POI_trigrams_05 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM World_POI_trigrams_05 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;
\copy World_POI_graph_10nn_trigrams_05 TO 'World_POI_graph_10nn_trigrams_0.5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- ------------------------------------------------------------------------ World-POI-trigrams_0.3.csv
CREATE TABLE World_POI_trigrams_03 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_trg > 0.3;
CREATE INDEX IF NOT EXISTS World_POI_trigrams_03_gix ON World_POI_trigrams_03 USING GIST (fsq_geom);
\copy World_POI_trigrams_03 TO 'World_POI_trigrams_0.3.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
-- World-POI-graph_10nn-trigrams_0.3.csv
CREATE TABLE World_POI_graph_10nn_trigrams_03 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM World_POI_trigrams_03 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM World_POI_trigrams_03 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;
\copy World_POI_graph_10nn_trigrams_03 TO 'World_POI_graph_10nn_trigrams_0.3.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- ------------------------------------------------------------------------The following datasets was huge and we decided not to publish them

-- ------------------------------------------------------------------------ World-POI-levenshtein_0.1.csv
CREATE TABLE World_POI_levenshtein_01 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.1;
CREATE INDEX IF NOT EXISTS World_POI_levenshtein_01_gix ON World_POI_levenshtein_01 USING GIST (fsq_geom);
\copy World_POI_levenshtein_01 TO 'World_POI_levenshtein_0.1.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
-- World-POI-graph_10nn-levenshtein_0.1.csv
CREATE TABLE World_POI_graph_10nn_levenshtein_01 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM World_POI_levenshtein_01 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM World_POI_levenshtein_01 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;
\copy World_POI_graph_10nn_levenshtein_01 TO 'World_POI_graph_10nn_levenshtein_0.1.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- ------------------------------------------------------------------------ World-POI-trigrams_0.1.csv
CREATE TABLE World_POI_trigrams_01 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_trg > 0.1;
CREATE INDEX IF NOT EXISTS World_POI_trigrams_01_gix ON World_POI_trigrams_01 USING GIST (fsq_geom);    
\copy World_POI_trigrams_01 TO 'World_POI_trigrams_0.1.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);
-- World-POI-graph_10nn-trigrams_0.1.csv
CREATE TABLE World_POI_graph_10nn_trigrams_01 AS
SELECT
  s.fsq_place_id  AS fsq_place_id_source,
  d.fsq_place_id  AS fsq_place_id_destination,
  ST_Distance(s.fsq_geom::geography, d.fsq_geom::geography) AS distance_m
FROM World_POI_trigrams_01 AS s
JOIN LATERAL (
  SELECT fsq_place_id, fsq_geom
  FROM World_POI_trigrams_01 AS d
  WHERE d.fsq_place_id <> s.fsq_place_id
  ORDER BY s.fsq_geom <-> d.fsq_geom
  LIMIT 10
) AS d ON TRUE;
\copy World_POI_graph_10nn_trigrams_01 TO 'World_POI_graph_10nn_trigrams_0.1.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);








