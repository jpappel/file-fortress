import pytest
from src.StorageManagers import LocalStorageManager
from unittest.mock import Mock, patch
from .classes import db_returns, LocalStorageManagerTest


@pytest.fixture
def db_ses():
    return db_returns()


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def local_storage_manager(db_ses, temp_dir):
    return LocalStorageManager(db_ses, temp_dir)


def test_none_raises_file_not_found(local_storage_manager):
    with pytest.raises(FileNotFoundError):
        local_storage_manager.lookup_link('test.png')


def test_allocate_url(local_storage_manager):
    real_url = local_storage_manager.allocate_url('test', 'test.png') 
    expected_url = 'test/test.png'
    assert real_url == expected_url


def test_allocate_url_with_exisiting_file():
    mock = Mock()
    mock.side_effect = [True, False]  # the first call will return True, and the second will return False
    with patch('src.StorageManagers.Path.exists', mock):
        manager = LocalStorageManagerTest()
        assert manager.allocate_url('test', 'test.png') == 'test/test.png_1'
