from src.db import get_db
from src.StorageManagers import LocalStorageManager


class Config(object):
    """
    Base Configuration for File Fortress
    """
    DEBUG = False
    TESTING = False
    # FIXME: generate a random secret key
    SECRET_KEY = 'demo_secret_key'
    DB = None


class TestConfig(Config):
    DEBUG = True
    TESTING = True


def production_config() -> Config:
    class ProductionConfig(Config):
        DB = get_db()
        STORAGE_ROOT = '/mnt/file_storage'
        STORAGE_MANAGER = LocalStorageManager(DB, STORAGE_ROOT)

    return ProductionConfig()
