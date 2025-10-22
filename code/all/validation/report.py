
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams
import os
CJK_PATH = "/usr/share/fonts/google-noto-sans-cjk-fonts/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(CJK_PATH)
CJK_PROP = fm.FontProperties(fname=CJK_PATH)
CJK_NAME = CJK_PROP.get_name()
rcParams['font.family'] = [CJK_NAME,'Noto Sans', 'Arial', 'sans-serif']
rcParams['axes.unicode_minus'] = False
# increase default font size
rcParams['font.size'] = 13
rcParams['figure.dpi'] = 600
rcParams['figure.figsize'] = (10, 6)

def _finish_plot(save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

def plot_region_distribution(data_table, save_path=None, top_n=20):
    df = data_table.select(['fsq_region']).to_pandas()
    counts = df['fsq_region'].dropna().astype(str).value_counts().head(top_n)
    # plt.figure(figsize=(10,8))
    plt.barh(counts.index[::-1], counts.values[::-1])
    plt.xlabel("Count")
    plt.ylabel("Region")
    _finish_plot(save_path)

def plot_locality_distribution(data_table, save_path=None, top_n=20):
    df = data_table.select(['fsq_locality']).to_pandas()
    counts = df['fsq_locality'].dropna()
    counts =  counts.astype(str)
    counts = counts.value_counts().head(top_n)
    # plt.figure(figsize=(10,8))
    plt.barh(counts.index[::-1], counts.values[::-1])
    plt.xlabel("Count")
    plt.ylabel("Locality")
    _finish_plot(save_path)

def plot_category_by_country(data_table, save_path=None, country=None, top_n=15):
    df = data_table.select(['fsq_country', 'fsq_category_labels']).to_pandas()
    sub = df.dropna(subset=['fsq_country', 'fsq_category_labels'])
    if country:
        sub = sub[sub['fsq_country'] == country]
    cats = sub['fsq_category_labels'].astype(str)
    counts = cats.value_counts().head(top_n)
    # plt.figure(figsize=(10,8))
    sns.barplot(y=counts.index, x=counts.values, orient="h")
    plt.xlabel("Count")
    plt.ylabel("Category")
    _finish_plot(save_path)

def plot_osm_class_distribution(data_table, save_path=None, top_n=20):
    df = data_table.select(['osm_class']).to_pandas()
    counts = df['osm_class'].dropna().astype(str).value_counts().head(top_n)
    # plt.figure(figsize=(10,8))
    plt.barh(counts.index[::-1], counts.values[::-1])
    plt.xlabel("Count")
    plt.ylabel("OSM Class")
    _finish_plot(save_path)


def plot_distance_hist(data_table, save_path=None):
    df = data_table.select(['fsq_osm_distance']).to_pandas()
    s = pandas.to_numeric(df['fsq_osm_distance'], errors='coerce').dropna()
    # plt.figure(figsize=(10,6))
    plt.hist(s, bins=40)
    plt.xlabel("Distance (degrees)")
    plt.ylabel("Count")
    _finish_plot(save_path)

def plot_name_similarity_hist(data_table, save_path=None):
    df = data_table.select(['fsq_osm_name_similarity_score']).to_pandas()
    s = pandas.to_numeric(df['fsq_osm_name_similarity_score'], errors='coerce').dropna()
    # plt.figure(figsize=(10,6))
    plt.hist(s, bins=40)
    plt.xlabel("Name similarity score")
    plt.ylabel("Count")
    _finish_plot(save_path)

def plot_country_distribution(data_table, save_path=None, top_n=20):
    df = data_table.select(['fsq_country']).to_pandas()
    counts = df['fsq_country'].dropna().astype(str).value_counts().head(top_n)
    # plt.figure(figsize=(10,8))
    plt.barh(counts.index[::-1], counts.values[::-1])
    plt.xlabel("Count")
    plt.ylabel("Country")
    _finish_plot(save_path)

def plot_count_per_year(data_table, col='fsq_date_created', save_path=None):
    df = data_table.select([col]).to_pandas()
    dates = pandas.to_datetime(df[col], errors='coerce', utc=True).dropna()
    counts = dates.dt.year.value_counts().sort_index()
    # plt.figure(figsize=(10,6))
    plt.bar(counts.index.astype(str), counts.values)
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    _finish_plot(save_path)

