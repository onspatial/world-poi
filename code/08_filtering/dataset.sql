-- World_POI_levenshtein_0.5
CREATE TABLE World_POI_levenshtein_05 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.5;
CREATE INDEX IF NOT EXISTS World_POI_levenshtein_05_gix ON World_POI_levenshtein_05 USING GIST (fsq_geom);
-- World_POI_levenshtein_0.3
CREATE TABLE World_POI_levenshtein_03 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.3;
CREATE INDEX IF NOT EXISTS World_POI_levenshtein_03_gix ON World_POI_levenshtein_03 USING GIST (fsq_geom);

-- World-POI-trigrams_0.5
CREATE TABLE World_POI_trigrams_05 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_trg > 0.5;
CREATE INDEX IF NOT EXISTS World_POI_trigrams_05_gix ON World_POI_trigrams_05 USING GIST (fsq_geom);

-- World-POI-trigrams_0.3
CREATE TABLE World_POI_trigrams_03 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_trg > 0.3;
CREATE INDEX IF NOT EXISTS World_POI_trigrams_03_gix ON World_POI_trigrams_03 USING GIST (fsq_geom);


--The following datasets was huge and we decided not to publish them

-- World-POI-levenshtein_0.1
CREATE TABLE World_POI_levenshtein_01 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_lev > 0.1;
CREATE INDEX IF NOT EXISTS World_POI_levenshtein_01_gix ON World_POI_levenshtein_01 USING GIST (fsq_geom);

-- World-POI-trigrams_0.1
CREATE TABLE World_POI_trigrams_01 AS
SELECT *
FROM fsq_osm
WHERE fsq_osm_name_similarity_score_trg > 0.1;
CREATE INDEX IF NOT EXISTS World_POI_trigrams_01_gix ON World_POI_trigrams_01 USING GIST (fsq_geom);    



