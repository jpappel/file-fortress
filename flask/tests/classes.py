from src.StorageManagers import LocalStorageManager

class db_returns:
    def __init__(self, val: dict = {}):
        val["id"] = 0
        self.val = val

    def cursor(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def connection(self, *args):
        return self

    def execute(self, query, *args):
        return None

    def fetchone(self):
        return self.val

    def close(self):
        pass
    def begin(self):
        pass
    def commit(self):
        pass


class LocalStorageManagerTest(LocalStorageManager):
    def __init__(self, val: dict = {}):
        super().__init__(db_returns(val), "")