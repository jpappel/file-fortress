import datetime
import os
from unittest.mock import Mock, patch
from flask import Flask, current_app
from pymysql import Timestamp
import pytest
import uuid
from src.StorageManagers import LocalStorageManager

from src import create_app
from src.configurations import TestConfig
from src.file_routes import file_api


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(file_api)
    app.config["DB"] = db_returns()
    app.config["STORAGE_MANAGER"] = LocalStorageManagerTest()
    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


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


def test_file_not_found(app, client, mocker):
    # Mock the database connection
    mocker.patch(
        "src.StorageManagers.LocalStorageManager.lookup_link",
        side_effect=FileNotFoundError,
    )

    # Mock the LocalStorageManager instantiation to use the mocked database connection
    # with patch('src.StorageManagers.LocalStorageManager.__init__', lambda x, db: None):
    db_mock = db_returns()
    with app.app_context():  # Set up the application context
        response = client.get("/api/v1/file/non_existent_file")

    assert response.status_code == 404
    assert response.json == {"error": "file not found"}


# def test_file_not_found(client, mocker):
#     # mock the value from get_file
#     app.DB = mocker.MagicMock()
#     response = client.get("/api/v1/file/test")
#     assert response.status_code == 404
#     assert {"error": "file not found"} == response.json


def test_delete_non_existing_file(app, client):
    with app.app_context():  # Set up the application context
        response = client.delete("/api/v1/file/test")
    assert response.status_code == 404
    assert {"error": "file not found"} == response.json


def test_upload_missing_file(app, client, mocker):
    with app.app_context():
        app.config["DB"] = db_returns()
    response = client.post("/api/v1/file/test.png")
    assert response.status_code == 400
    assert response.json == {"error": "no file provided"}


# @pytest.mark.skip(reason="storage manager and db not mocked")
def test_upload_file(client, mocker, tmpdir):
    # create dummy test file
    p = tmpdir.mkdir("test") / "test.txt"
    p.write("testing body")

    # setup request
    files = {"file": (p.open("rb"),"test.txt")}
    params = {"privacy": "public", "expires": 1700824992}

    response = client.post(
        "/api/v1/file/test", data=files, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json == {"success": "file uploaded succesfully"}
    os.remove('0/test.txt')
    os.rmdir('0')

# @pytest.mark.skip(reason="not sure how to make this mock yet")
def test_file_found(app, client, mocker):
    # mock the value from get_file
    expected_return = {
        "id": 1,
        "uploader_id": str(uuid.uuid4()),
        "short_link": "test.png",
        "url": "https://example.com/test.png",
        "mime_type": "image/png",
        "expires": None,
        "privacy": "public",
        "modified_date": datetime.datetime.now(),
        "created_date": datetime.datetime.now(),
    }
    with app.app_context():  # Set up the application context
        app.config["DB"] = db_returns(expected_return)
    response = client.get("/api/v1/file/test.png/info")
    print(response)
    assert response.status_code == 200
    assert expected_return == response.json
