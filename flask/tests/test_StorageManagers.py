import pytest
from src.StorageManagers import LocalStorageManager

class db_returns():
    def __init__(self,val):
        self.val = val
        pass
    def cursor(self):
        return self
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return None
    def execute(self,query, *args):
        return None
    def fetchone(self):
        return self.val

def test_StorageManager():
    manager = LocalStorageManager(db_returns(None),'')
    
def test_none_raises_file_not_found():
    manager = LocalStorageManager(db_returns(None),'')
    with pytest.raises(FileNotFoundError):
        manager.lookup_link('test.png')

def test_lookup_link():
    manager = LocalStorageManager(db_returns({'url':'test.png'}),'')
    assert manager.lookup_link('test.png') == 'test.png'

