import os
def download_foursquare():
    if os.path.exists("data/downloaded/places/places-00000.zstd.parquet"):
        print("Data already downloaded. Skipping download.")
        return
    print("Downloading the parquet files...")
    # os.system("sudo dnf install -y awscli2")
    os.system("aws s3 cp --no-sign s3://fsq-os-places-us-east-1/release/dt=2025-07-08/places/parquet data/downloaded/places/ --recursive")
    os.system("aws s3 cp --no-sign s3://fsq-os-places-us-east-1/release/dt=2025-07-08/categories/parquet data/downloaded/categories/ --recursive")
    print("Download complete.")

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

if __name__ == "__main__":
    initialize()
    