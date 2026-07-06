

import pandas 




def at_once(input_file, output_file, score, distance):
    base_df = pandas.read_csv(input_file)
    new_df = base_df[(base_df["fsq_osm_name_similarity_score_lev"] >= score) & (base_df["fsq_osm_distance"] < distance)]
    new_df.to_csv(output_file, index=False)
    return new_df

def lev_at_chunks(input_file, output_file, score, distance, name_similarity_col="fsq_osm_name_similarity_score_lev", distance_col="fsq_osm_distance"):
    # do it in chunk:
    res_df = []
    for chunk in pandas.read_csv(input_file, chunksize=10):
        new_df = chunk[(chunk[name_similarity_col] >= score) & (chunk[distance_col] < distance)]
        res_df.append(new_df)
    res_df = pandas.concat(res_df)
    res_df.to_csv(output_file, index=False)
    return res_df

if __name__ == "__main__":
    

    df1 = at_once('data/World_POI_levenshtein_0.5_small.csv', 'data/World_POI_levenshtein_0.5_small1.csv', 0.1, 0.00025)
    df2 = lev_at_chunks('data/World_POI_levenshtein_0.5_small.csv', 'data/World_POI_levenshtein_0.5_small3.csv', 0.1, 0.00025)

    # diff
    # sort both by fsq_place_id
    df1 = df1.sort_values(by=['fsq_place_id'])
    df2 = df2.sort_values(by=['fsq_place_id'])
    diff = pandas.concat([df1, df2]).drop_duplicates(keep=False)
    print("diff: ", diff)