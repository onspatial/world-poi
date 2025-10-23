-- World_POI_levenshtein_0.5.csv
\copy World_POI_levenshtein_05 TO 'World_POI_levenshtein_0.5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- World_POI_levenshtein_0.3.csv
\copy World_POI_levenshtein_03 TO 'World_POI_levenshtein_0.3.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- World-POI-trigrams_0.5.csv
\copy World_POI_trigrams_05 TO 'World_POI_trigrams_0.5.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- World-POI-trigrams_0.3.csv
\copy World_POI_trigrams_03 TO 'World_POI_trigrams_0.3.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

--The following datasets was huge and we decided not to publish them

-- World-POI-levenshtein_0.1.csv
\copy World_POI_levenshtein_01 TO 'World_POI_levenshtein_0.1.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);

-- World-POI-trigrams_0.1.csv
\copy World_POI_trigrams_01 TO 'World_POI_trigrams_0.1.csv' WITH (FORMAT csv, HEADER, QUOTE '"', ESCAPE '"', NULL '', FORCE_QUOTE *);






