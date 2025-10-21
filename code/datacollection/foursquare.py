import pandas
import pyarrow.parquet as pyarrow_parquet
import os
import time
import csv
def print_time(*args, **kwargs):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{current_time}]: ", *args, **kwargs)


def get_raw_data_df(raw_data_path="data/foursquare.csv", refresh=False):
    if os.path.exists(raw_data_path) and not refresh:
        print_time(f"File {raw_data_path} already exists. Loading existing data.")
        raw_data_df = pandas.read_csv(raw_data_path,  dtype=str, encoding='utf-8', engine='python')
    else:
        raw_data_list = []
        for i in range(100):
            csv_path = f"data/converted/places/places-{i:05d}.csv"
            if os.path.exists(csv_path) and not refresh:
                print_time(f"File {csv_path} already exists... loading existing data.")
                table_df = pandas.read_csv(csv_path,  dtype=str, encoding='utf-8',engine='python')
            else:
                print_time(f"Converting file {i} to {csv_path}...")
                table_pq = pyarrow_parquet.read_table(f"data/downloaded/places/places-{i:05d}.zstd.parquet")
                table_pq = table_pq.drop(["geom"])
                table_df = table_pq.to_pandas()
                table_df.to_csv(csv_path, index=False, encoding='utf-8')

            raw_data_list.append(table_df)
        raw_data_df = pandas.concat(raw_data_list, ignore_index=True)
        raw_data_df.to_csv(raw_data_path, index=False, encoding='utf-8')
    print_time(f"Loaded {len(raw_data_df)} rows and {len(raw_data_df.columns)} columns from {raw_data_path}")
    print_time(raw_data_df.head())
    return raw_data_df


def download_foursquare():
    if os.path.exists("data/downloaded/places/places-00000.zstd.parquet"):
        print_time("Data already downloaded. Skipping download.")
        return
    print_time("Downloading the parquet files...")
    # os.system("sudo dnf install -y awscli2")
    os.system("aws s3 cp --no-sign s3://fsq-os-places-us-east-1/release/dt=2025-07-08/places/parquet data/downloaded/places/ --recursive")
    os.system("aws s3 cp --no-sign s3://fsq-os-places-us-east-1/release/dt=2025-07-08/categories/parquet data/downloaded/categories/ --recursive")
    print_time("Download complete.")

def make_directories():
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/downloaded", exist_ok=True)
        os.makedirs("data/downloaded/places", exist_ok=True)
        os.makedirs("data/downloaded/categories", exist_ok=True)
        os.makedirs("data/converted", exist_ok=True)
        os.makedirs("data/converted/places", exist_ok=True)
        os.makedirs("data/converted/categories", exist_ok=True)
        return True
    except:
        return False

def initialize():
    make_directories()
    download_foursquare()

def save_clean_data(raw_data_df, clean_data_path):
    clean_data_df = raw_data_df.copy()
    clean_data_df.columns = [f"fsq_{col}" if not col.startswith("fsq_") else col for col in clean_data_df.columns]
    print_time(f"Cleaned column names: {clean_data_df.columns.tolist()}")
    # use "" for all string columns
    clean_data_df.to_csv(clean_data_path, index=False, quoting=csv.QUOTE_ALL, quotechar='"')

if __name__ == "__main__":
    initialize()
    raw_data_path = "data/foursquare.csv"
    clean_data_path = "data/foursquare_clean.csv"
    raw_data_df = get_raw_data_df()
    save_clean_data(raw_data_df, clean_data_path)