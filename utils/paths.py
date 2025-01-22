from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
CONFIG_PATH = ROOT_PATH / 'configs'
URL_CONFIG_PATH = CONFIG_PATH / 'url_config.json'
DATA_PATH = ROOT_PATH / 'data'
BOOKS_PATH = DATA_PATH / 'books'