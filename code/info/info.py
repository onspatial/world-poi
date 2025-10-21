import pandas as pd
from ast import literal_eval

# Load dataset
df = pd.read_csv("fsq_osm_usa_name_filtered_5.csv")

# Basic stats
print("Total Matched Entries:", len(df))
print("FSQ-OSM Name Similarity Score - mean:", df['fsq_osm_name_similarity_score'].mean())
print("FSQ-OSM Name Similarity Score - std:", df['fsq_osm_name_similarity_score'].std())
print("FSQ-OSM Name Similarity Score - min:", df['fsq_osm_name_similarity_score'].min())
print("FSQ-OSM Name Similarity Score - max:", df['fsq_osm_name_similarity_score'].max())

print("FSQ-OSM Distance (m) - mean:", df['fsq_osm_distance'].mean())
print("FSQ-OSM Distance (m) - std:", df['fsq_osm_distance'].std())
print("FSQ-OSM Distance (m) - min:", df['fsq_osm_distance'].min())
print("FSQ-OSM Distance (m) - max:", df['fsq_osm_distance'].max())

# Safely parse category labels
def safe_parse(val):
    try:
        if pd.notnull(val):
            return literal_eval(val)
    except:
        return []
    return []

df['parsed_labels'] = df['fsq_category_labels'].apply(safe_parse)

# Count top categories
all_labels = df['parsed_labels'].explode()
top_categories = all_labels.value_counts().head(10)

print("\nTop 10 POI Categories:")
print(top_categories)
