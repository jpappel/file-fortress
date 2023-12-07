import pytest
import sqlite3
from src.StorageManagers import LocalStorageManager
from unittest.mock import Mock, patch, mock_open

class db_returns():
    def __init__(self, val: dict = {}):
        val['id'] = 0
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
    
class LocalStorageManagerTest(LocalStorageManager):
    def __init__(self, val: dict = {}):
        super().__init__(db_returns(val), "")
    def lookup_link(self, short_link: str) -> str:
        return 


@pytest.fixture
def db_ses():
    return db_returns()


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def local_storage_manager(db_ses, temp_dir):
    return LocalStorageManager(db_ses, temp_dir)

# class LocalStorageManagerTest(LocalStorageManager):
#     def __init__(self, dict: dict = {}):
#         super().__init__(db_returns(dict), "")


# class db_returns():
#     def __init__(self, val: dict = {}):
#         val['id'] = 0
#         self.val = val
#
#     def cursor(self):
#         return self
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, *args):
#         return None
#
#     def execute(self, query, *args):
#         return None
#
#     def fetchone(self):
#         return self.val


# def test_StorageManager():
#     manager = LocalStorageManagerTest()


def test_none_raises_file_not_found(local_storage_manager):
    with pytest.raises(FileNotFoundError):
        local_storage_manager.lookup_link('test.png')


# def test_lookup_link(local_storage_manager):
#     # TODO: put (shortlink, url) into db mock
#     local_storage_manager.db.lookup_link
#     url = local_storage_manager.lookup_link('short_link')
#     assert url == 'test.png'


# def test_allocate_url(local_storage_manager):
#     real_url = local_storage_manager.allocate_url('test', 'test.png') 
#     expected_url = 'test/test.png'
#     assert real_url == expected_url
#     with patch('pathlib.Path.exists', return_value=True):
#         real_url = local_storage_manager.allocate_url('test','test.png')
#         expected_url = 'test/test.png_1'
#         assert real_url == expected_url


# def test_allocate_url_with_exisiting_file():
#     mock = Mock()
#     mock.side_effect = [True, False]  # the first call will return True, and the second will return False
#     with patch('src.StorageManagers.Path.exists', mock):
#         manager = LocalStorageManagerTest()
#         assert manager.allocate_url('test', 'test.png') == 'test/test.png_1'
