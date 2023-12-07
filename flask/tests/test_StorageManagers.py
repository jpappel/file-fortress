import pytest
import sqlite3
from src.StorageManagers import LocalStorageManager
from unittest.mock import Mock, patch, mock_open


class TestDB:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE users (
        id INT AUTO_INCREMENT,
        name VARCHAR(31) NOT NULL,
        upload_limit INT UNSIGNED, -- NULL is no limit
        collection_limit INT UNSIGNED DEFAULT 31,
        collection_size_limit INT UNSIGNED DEFAULT 15,
        PRIMARY KEY (id),
        CONSTRAINT check_positive_upload_limit
            CHECK (upload_limit > 0 OR upload_limit IS NULL),
        CONSTRAINT check_positive_collection_limit
            CHECK (collection_limit > 0 OR collection_limit IS NULL),
        CONSTRAINT check_positive_collection_size_limit
            CHECK (collection_size_limit > 0 OR collection_size_limit IS NULL)
        )''')
        self.conn.commit()
        cursor.execute('''
        CREATE TABLE files (
        id INT AUTO_INCREMENT,
        uploader_id INT,
        short_link VARCHAR(255) UNIQUE NOT NULL,
        url VARCHAR(255),
        mime_type VARCHAR(31),
        expires DATETIME,
        privacy VARCHAR(7) DEFAULT 'public' NOT NULL,
        modified_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY (uploader_id) REFERENCES users(id)
        )''')
        self.conn.commit()
        cursor.execute('INSERT INTO USERS (name, collection_limit, collection_size_limit) VALUES ("system", NULL, NULL);')
        self.conn.commit()
        # base = '../../mariadb/'
        # files = ('init.sql', 'procedures.sql', 'default_files.sql')
        # for path in map(lambda file: base + file, files):
        #     with open(path, 'r') as f:
        #         contents = f.read()
        #
        #     self.conn.executescript(contents)
        #
        #     self.conn.commit()

    def connection(self) -> sqlite3.Connection:
        return self.conn


@pytest.fixture
def db_ses():
    return TestDB()


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
