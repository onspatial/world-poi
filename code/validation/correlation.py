from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
import h3
import numpy
import pandas
import rasterio
import pyarrow
import pyarrow.parquet as pq

def get_grid_naive(input_df, grid_level=1):
    df = input_df.copy()
    grid_size = get_naive_grid_size(grid_level)
    df["longitude_grid"] = (df["longitude"] // grid_size) * grid_size
    df["latitude_grid"] = (df["latitude"] // grid_size) * grid_size
    grid_df = df.groupby(["longitude_grid", "latitude_grid"], as_index=False)['value'].sum()
    return grid_df

def get_naive_grid_size(grid_level):
    if grid_level == 15:
        return 0.00000525
    elif grid_level == 14:
        return 0.0000139
    elif grid_level == 13:
        return 0.0000367
    elif grid_level == 12:
        return 0.000097
    elif grid_level == 11:
        return 0.000258
    elif grid_level == 10:
        return 0.000682
    elif grid_level == 9:
        return 0.00181
    elif grid_level == 8:
        return 0.00477
    elif grid_level == 7:
        return 0.0127
    elif grid_level == 6:
        return 0.0334
    elif grid_level == 5:
        return 0.0885
    elif grid_level == 4:
        return 0.234
    elif grid_level == 3:
        return 0.62
    elif grid_level == 2:
        return 1.64
    elif grid_level == 1:
        return 4.34
    elif grid_level == 0:
        return 11.5
    else:
        raise ValueError(f"Unsupported grid level: {grid_level}. Supported levels are 0 to 15.")

def get_grid(input_df, grid_level=1,which="h3"):
    if which == "h3":
        return get_grid_h3(input_df, resolution=grid_level)
    else:
        return get_grid_naive(input_df, grid_level=grid_level)
    
def get_grid_h3(df, resolution=0):
    df = df.copy()
    df["h3_cell"] = [
        h3.latlng_to_cell(lat, lon, resolution)
        for lat, lon in zip(df["latitude"], df["longitude"])
    ]

    value_cols = [col for col in df.columns if col not in ["longitude", "latitude", "h3_cell"]]
    grid_df = df.groupby("h3_cell", as_index=False)[value_cols].sum()
    return grid_df

def get_df(path):
    if path.endswith(".csv"):
        return pandas.read_csv(path)
    elif path.endswith(".parquet"):
        return pandas.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file format for path: {path}")
def save_df(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.endswith(".csv"):
        df.to_csv(path, index=False)
    elif path.endswith(".parquet"):
        df.to_parquet(path, index=False)
    else:
        raise ValueError(f"Unsupported file format for path: {path}")

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)
       
def get_worldpop_df(data_path="data/worldpop.tif"):
    save_path = "data/intermediate/renamed_worldpop.csv"
    if os.path.exists(save_path):
        return get_df(save_path)

    with rasterio.open(data_path) as src:
        arr = src.read(1)
        nodata = src.nodata

        if nodata is None:
            valid_mask = numpy.isfinite(arr)
        else:
            valid_mask = (arr != nodata) & numpy.isfinite(arr)

        rows, cols = numpy.where(valid_mask)
        xs, ys = rasterio.transform.xy(src.transform, rows, cols)

        population_df = pandas.DataFrame(
            {
                "longitude": xs,
                "latitude": ys,
                "value": arr[rows, cols],
            }
        )

    population_df = population_df[population_df["value"] > 1000].copy()
    save_df(population_df, save_path)
    return population_df

def get_population_df(keep_population_value=False):
    save_path = "data/intermediate/renamed_population.csv"
    if os.path.exists(save_path):
        return get_df(save_path)
    population_df = get_df("data/population.csv")
    population_df = population_df.rename(
        columns={"X": "longitude", "Y": "latitude", "population": "value"}
    )
    population_df = population_df[["longitude", "latitude", "value"]]
    if not keep_population_value:
        population_df["value"] = 1
    save_df(population_df, save_path)
    return population_df

def get_advan_df():
    save_path = "data/intermediate/renamed_advan.csv"
    if os.path.exists(save_path):
        return get_df(save_path)
    advan_df = get_df("data/advan.csv")
    advan_df = get_renamed_df(advan_df)
    save_df(advan_df, save_path)
    return advan_df

def get_worldpoi_df(t=5, category="all", similarity_algorithm="levenshtein"):
    save_path = f"data/intermediate/renamed_{similarity_algorithm}_{t}_{category}.parquet"
    if os.path.exists(save_path):
        return get_df(save_path)

    poi_df = get_poi_df(t=t, category=category, similarity_algorithm=similarity_algorithm)
    poi_df = get_renamed_df(poi_df)
    save_df(poi_df, save_path)
    return poi_df

def get_poi_df(t=5, category="all",similarity_algorithm="levenshtein"):
    save_path = f"data/intermediate/poi_{t}_{similarity_algorithm}_{category}.parquet"
    save_path_all = f"data/intermediate/poi_{t}_{similarity_algorithm}_all.parquet"
    if os.path.exists(save_path):
        return get_df(save_path)
    elif category == "all":
       return get_in_chunks(input_path = f"data/World_POI_{similarity_algorithm}_0.{t}.csv", save_path = save_path_all)
    else:
        all_df = get_in_chunks(input_path = f"data/World_POI_{similarity_algorithm}_0.{t}.csv", save_path = save_path_all)
        return get_filtered_df(all_df, category, save_path)
    
def get_renamed_df(df):
    df = df.copy()
    df.columns  = [col.lower() for col in df.columns]
    if "fsq_latitude" in df.columns and "fsq_longitude" in df.columns:  
        df = df.rename(columns={"fsq_latitude": "latitude", "fsq_longitude": "longitude"})

    if "lat" in df.columns and "lon" in df.columns:
        df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
    
    required_cols = {"longitude", "latitude"}
    missing = required_cols - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if "population" in df.columns:
        df = df.rename(columns={"population": "value"})
    else:
        df["value"] = 1
    df = df[["longitude", "latitude", "value"]]
    
    return df

def int_me(x):
    try:
        return int(x)
    except:
        return 0

def align_grid_values(*named_grid_dfs,join_cols=["h3_cell"], id=""):
    merged = None
    save_path = f"data/analysis/intermediate/aligned_grid_values_{id}.parquet"
    for name, grid_df in named_grid_dfs:
        current = grid_df[join_cols + ["value"]].rename(columns={"value": name})
        if merged is None:
            merged = current
        else:
            merged = merged.merge(current, on=join_cols, how="outer")
    if 'mask' in merged.columns:
        merged['mask'] = merged.apply(lambda row: 1 if any(int_me(row[col]) > 0 for col in merged.columns if col not in['mask', 'h3_cell', 'longitude_grid', 'latitude_grid']) else 0, axis=1)
    merged = merged.fillna(0)
    save_df(merged, save_path)
    return merged

def get_mask_df(grid_level=1):
    grid_size = get_naive_grid_size(grid_level)
    save_path = f"data/analysis/intermediate/grid_baseline_{grid_level}.parquet"
    if os.path.exists(save_path):
        return get_df(save_path)
    lon_range = numpy.arange(-180, 180, grid_size)
    lat_range = numpy.arange(-90, 90, grid_size)
    grid_df = pandas.DataFrame(
        [(lon, lat) for lon in lon_range for lat in lat_range],
        columns=["longitude", "latitude"]
    )
    grid_df["value"] = 0
    save_df(grid_df, save_path)
    return grid_df

def safe_corr(df, col_a, col_b):
    if col_a not in df.columns or col_b not in df.columns:
        return numpy.nan

    if len(df) == 0:
        print(f"Warning: DataFrame is empty when calculating correlation between {col_a} and {col_b}. Returning NaN.")
        return numpy.nan

    if df[col_a].nunique() <= 1 or df[col_b].nunique() <= 1:
        print(f"Warning: One of the columns ({col_a} or {col_b}) has zero variance when calculating correlation. Returning NaN.")
        return numpy.nan

    return df[col_a].corr(df[col_b])

def get_in_chunks(input_path = "data/World_POI_levenshtein_0.3.csv", save_path = "data/intermediate/poi_3_levenshtein.parquet"):
    first_chunk = True
    
    if os.path.exists(save_path):
        return get_df(save_path)
    
    csv_save_path = save_path.replace(".parquet", ".csv")
    usecols = ["fsq_latitude", "fsq_longitude", "fsq_category_ids","fsq_category_labels"]
    
    for chunk in pandas.read_csv(
        input_path,
        usecols=usecols,
        chunksize=1_000_000,
    ):

        chunk.to_csv(
            csv_save_path,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )
        first_chunk = False
    df = get_df(csv_save_path)
    save_df(df, save_path)
    return df

def get_filtered_df(all_df, category, save_path):
    if os.path.exists(save_path):
        return get_df(save_path)
    filtered_df = all_df[all_df["fsq_category_ids"].str.contains(category, case=False, na=False)]
    save_df(filtered_df, save_path)      
    return filtered_df
    
def get_results_category(category, grid_level=0):
    
    results_categories = []
    for t in [5]:
        levenshtein_df = get_worldpoi_df(t=t, category=category, similarity_algorithm="levenshtein")
        trigrams_df = get_worldpoi_df(t=t, category=category, similarity_algorithm="trigrams")
        baseline_df = get_population_df()
        

        for grid_algorithm in ["h3"]:
            result_path = f"data/insight/results/result_c_{category}_t_{t}_gl_{grid_level}_ga_{grid_algorithm}.json"
            if os.path.exists(result_path):
                result = load_json(result_path)
            else:
                baseline_grid_df = get_grid(baseline_df, grid_level=grid_level, which=grid_algorithm)
                levenshtein_grid_df = get_grid(levenshtein_df, grid_level=grid_level, which=grid_algorithm)
                trigrams_grid_df = get_grid(trigrams_df, grid_level=grid_level, which=grid_algorithm)
                mask_df = get_mask_df(grid_level=grid_level)
                mask_grid_df = get_grid(mask_df, grid_level=grid_level, which=grid_algorithm)

                join_cols = ["h3_cell"] if grid_algorithm == "h3" else ["longitude_grid", "latitude_grid"]

                aligned_df = align_grid_values(
                    ("mask", mask_grid_df),
                    ("baseline", baseline_grid_df),
                    ("levenshtein", levenshtein_grid_df),
                    ("trigrams", trigrams_grid_df),
                    join_cols=join_cols,
                    id=f"{t}_{grid_level}_{grid_algorithm}_{category}"

                )
                levenshtein_score = safe_corr(aligned_df, 'baseline', 'levenshtein')
                trigrams_score = safe_corr(aligned_df, 'baseline', 'trigrams')
                grid_degree = get_naive_grid_size(grid_level)
                result = {
                        "category": category,
                        "levenshtein_correlation": levenshtein_score,
                        "trigrams_correlation": trigrams_score,
                        "similarity_threshold": t,
                        "grid_level": grid_level,
                        "grid_degree": grid_degree,
                        "grid_edge_km": round(grid_degree * 111),
                        "grid_algorithm": grid_algorithm
                    }
                save_json(result, result_path)
            levenshtein_score = result.get("levenshtein_correlation", numpy.nan)
            trigrams_score = result.get("trigrams_correlation", numpy.nan)
            grid_degree = result.get("grid_degree", numpy.nan)
            grid_level = result.get("grid_level", numpy.nan)
            grid_edge_km = result.get("grid_edge_km", numpy.nan)
            if levenshtein_score> 0.25 or trigrams_score > 0.25:
                print(f"Similarity threshold: {t}, Category: {category}, Grid Level: {grid_level}, Grid edge: {grid_edge_km} KM, Grid algorithm: {grid_algorithm} -> Correlation for levenshtein & trigrams: {levenshtein_score:.4f} & {trigrams_score:.4f}")
                results_categories.append(result)
        return results_categories
    


def get_all_categories_dict():
    # downloaded from foursquare.com
    categories_df = pandas.read_csv("data/personalization-apis-movement-sdk-categories.csv")
    category_dict = {}
    for _, row in categories_df.iterrows():
        cat_id = row["Category ID"]
        cat_name = row["Category Name"]
        cat_label = row["Category Label"]
        category_dict[cat_id] = (cat_name, cat_label)
    print(f"Constructed category dictionary with {len(category_dict)} entries. Sample entries: {list(category_dict.items())[:10]}")
    return category_dict

def process_category(category, grid_level=0):
    try:
        return get_results_category(category, grid_level=grid_level) or []
    except Exception as e:
        print(f"Error processing category '{category}': {e}")
        return []
    
if __name__ == "__main__":
    os.makedirs("data/analysis/intermediate/", exist_ok=True)
    os.makedirs("data/intermediate/", exist_ok=True)
    category_dict = get_all_categories_dict()
    all_categories = ["all"] + list(category_dict.keys())
    grid_levels = [0, 1, 2, 3, 4, 5]
    for grid_level in grid_levels:
        top_categories = []
        with ProcessPoolExecutor(max_workers=1) as executor:
            futures = [
                executor.submit(get_results_category, category, grid_level=grid_level)
                for category in all_categories
            ]

            for future in as_completed(futures):
                top_categories.extend(future.result())
            
        top_categories = sorted(top_categories, key=lambda x: max(x["levenshtein_correlation"], x["trigrams_correlation"]), reverse=True)
        for result in top_categories:
            category_id = result["category"]
            category_info = category_dict.get(category_id, ("Unknown Category", "Unknown Label"))
            result["category_name"] = category_info[0]
            result["category_label"] = category_info[1]
            
            first_keys = ["category", "category_name", "category_label"]
            reordered = {
                k: result[k]
                for k in first_keys + [k for k in result if k not in first_keys]
            }

            result.clear()
            result.update(reordered)

        
        

        save_json(top_categories, f"data/analysis/top_categories_{grid_level}_h3.json")