from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
CONFIG_PATH = ROOT_PATH / 'configs'
URL_CONFIG_PATH = CONFIG_PATH / 'url_config.json'
DATA_PATH = ROOT_PATH / 'data'
BOOKS_PATH = DATA_PATH / 'books_data.csv'
AUTHORS_PATH = DATA_PATH / 'authors_data.csv'
UMAP_BESTSELLERS_PATH = DATA_PATH / 'umap_3d_bestseller.csv'
UMAP_CLUSTERS_PATH = DATA_PATH / 'umap_3d_clusters.csv'
PICS_PATH = DATA_PATH / 'pics'