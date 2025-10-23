UPDATE fsq_osm
SET fsq_osm_name_similarity_score_trg = GREATEST(similarity(LOWER(fsq_name), LOWER(osm_name)), 0.0);