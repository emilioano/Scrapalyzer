import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    # Base
    BASE_DIR = BASE_DIR
    DATA_DIR = os.path.join(BASE_DIR, "data")
    # Storage
    DOWNLOADS_DIR = os.path.join(DATA_DIR, "downloads")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    ANALYZED_DIR = os.path.join(DATA_DIR, "analyzed")
    # Modules
    MODULES_DIR = os.path.join(BASE_DIR, "modules")
    UTILS_DIR = os.path.join(MODULES_DIR, "utils")
    SCRAPER_DIR = os.path.join(MODULES_DIR, "scraper")
    ANALYZER_DIR = os.path.join(MODULES_DIR, "analyzer")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False