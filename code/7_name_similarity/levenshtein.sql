
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



UPDATE fsq_osm
SET fsq_osm_name_similarity_score_lev =
    levenshtein_similarity(fsq_name, osm_name);
