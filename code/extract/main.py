# this file can be used to filter the csv file based on the similarity score and distance

import os
import pandas


def get_dtype(similarity_col):
    return {
        "fsq_place_id": "string",
        "fsq_name": "string",
        "fsq_latitude": "float64",
        "fsq_longitude": "float64",
        "fsq_address": "string",
        "fsq_locality": "string",
        "fsq_region": "string",
        "fsq_postcode": "string",
        "fsq_admin_region": "string",
        "fsq_post_town": "string",
        "fsq_po_box": "string",
        "fsq_country": "string",
        "fsq_date_created": "string",
        "fsq_date_refreshed": "string",
        "fsq_date_closed": "string",
        "fsq_tel": "string",
        "fsq_website": "string",
        "fsq_email": "string",
        "fsq_facebook_id": "string",
        "fsq_instagram": "string",
        "fsq_twitter": "string",
        "fsq_category_ids": "string",
        "fsq_category_labels": "string",
        "fsq_placemaker_url": "string",
        "fsq_unresolved_flags": "string",
        "fsq_bbox": "string",
        "fsq_geom": "string",
        "osm_id": "string",
        "osm_class": "string",
        "osm_type": "string",
        "osm_name": "string",
        "osm_address": "string",
        "osm_extratags": "string",
        "osm_geometry": "string",
        "osm_latitude": "float64",
        "osm_longitude": "float64",
        "osm_geom": "string",
        similarity_col: "float64",
        "fsq_osm_distance" : "float64",
    }





def process(input_file, output_file, score, distance, chunksize=100000, similarity_col="fsq_osm_name_similarity_score_lev"):
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    
    if os.path.exists(output_file):
        print(f"Output file already exists, skipping: {output_file}")
        return
    
    print(f"Preparing file: {input_file} with score >= {score} and distance <= {distance}")

    first = True

    for chunk in pandas.read_csv(
        input_file,
        chunksize=chunksize,
        dtype=get_dtype(similarity_col=similarity_col),
        low_memory=False
    ):
        out = chunk[
            (chunk[similarity_col] >= score) &
            (chunk["fsq_osm_distance"] <= distance)
        ]

        out.to_csv(
            output_file,
            mode="w" if first else "a",
            header=first,
            index=False
        )

        first = False

if __name__ == "__main__":
    
    scores = [ 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    distances = [0.0015,  0.00125,  0.001, 0.0005, 0.00025]
    # score and distance should be sorted so previous data can be used to filter the next data for efficiency
    scores.sort()
    distances.sort(reverse=True)
    print(f"Scores: {scores}")
    print(f"Distances: {distances}")
    prev_score=0.3
    prev_distance=0.0015
    for score in scores:
        for distance in distances:
            print(f"Processing score: {score}, distance: {distance}")
            process(f'data/World_POI_levenshtein_{prev_score}_{prev_distance}.csv', f'data/World_POI_levenshtein_{score}_{distance}.csv', score, distance,similarity_col = "fsq_osm_name_similarity_score_lev")
            process(f'data/World_POI_trigrams_{prev_score}_{prev_distance}.csv', f'data/World_POI_trigrams_{score}_{distance}.csv', score, distance,similarity_col = "fsq_osm_name_similarity_score_trg")
            prev_distance=distance
            prev_score=score

