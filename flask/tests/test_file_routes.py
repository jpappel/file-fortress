from unittest.mock import Mock, patch
from flask import Flask, current_app
import pytest
import uuid

from src import create_app
from src.configurations import TestConfig
from src.file_routes import file_api


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(file_api)
    return app

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


def test_file_not_found(app, client, mocker):
    # Mock the database connection
    db_mock = Mock()
    mocker.patch('src.StorageManagers.LocalStorageManager.lookup_link', side_effect=FileNotFoundError)

    # Mock the LocalStorageManager instantiation to use the mocked database connection
    with patch('src.StorageManagers.LocalStorageManager.__init__', lambda x, db: None):
        with app.app_context():  # Set up the application context
            with patch('src.file_routes.current_app.config', {'DB': db_mock}):
                response = client.get("/api/v1/file/non_existent_file")

    assert response.status_code == 404
    assert response.json == {'error': 'file not found'}


# def test_file_not_found(client, mocker):
#     # mock the value from get_file
#     app.DB = mocker.MagicMock()
#     response = client.get("/api/v1/file/test")
#     assert response.status_code == 404
#     assert {"error": "file not found"} == response.json


def test_delete_non_existing_file(client, mocker):
    app.db = mocker.MagicMock()
    response = client.delete('/api/v1/file/test')
    assert response.status_code == 404
    assert {"error": "file not found"} == response.json


def test_upload_missing_file(client, mocker):
    app.db = mocker.MagicMock()
    response = client.post('/api/v1/file/test.png')
    assert response.status_code == 400
    assert response.json == {'error': 'no file provided'}


@pytest.mark.skip(reason="storage manager and db not mocked")
def test_upload_file(client, mocker, tmpdir):
    # mock components
    app.db = mocker.MagicMock()

    # create dummy test file
    p = tmpdir.mkdir('test')/'test.txt'
    p.write("testing body")

    # setup request
    files = {'file': ('test.txt', open(p, 'r'))}
    params = {'privacy': 'public', 'expires': 1700824992}

    response = client.post('/api/v1/file/test', files=files, params=params)

    assert response.status_code == 200
    assert response.json == {'success': 'file uploaded succesfully'}


@pytest.mark.skip(reason="not sure how to make this mock yet")
def test_file_found(client, mocker):
    # mock the value from get_file
    class db_returns:
        def __init__(self, val):
            self.val = val
            pass

        def cursor(self):
            return self

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def execute(self, query, *args):
            return None

        def fetchone(self):
            return self.val

    expected_return = {
        "id": 1,
        "uploader_id": str(uuid.uuid4()),
        "short_link": "test.png",
        "url": "https://example.com/test.png",
        "mime_type": "image/png",
        "expires": None,
        "privacy": "public",
        "modified_date": "2021-01-01 00:00:00",
        "created_date": "2021-01-01 00:00:00",
    }

    app.db = mocker.MagicMock(return_value=db_returns(expected_return))

    # return_value = expected_return
    response = client.get("/api/v1/file/test.png")
    assert response.status_code == 200
    assert expected_return == response.json
