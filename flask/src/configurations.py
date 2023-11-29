from .db import get_db
from .StorageManagers import LocalStorageManager


class Config(object):
    TESTING = False


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DB = get_db()
    STORAGE_ROOT = '/mnt/file_storage'
    STORAGE_MANAGER = LocalStorageManager(DB, STORAGE_ROOT)
