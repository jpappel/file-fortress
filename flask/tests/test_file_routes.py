import datetime
import os
from flask import Flask
import pytest
import uuid


from src.file_routes import file_api

from .classes import db_returns, LocalStorageManagerTest

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


def test_file_not_found(app, client, mocker):
    # Mock the database connection
    mocker.patch(
        "src.StorageManagers.LocalStorageManager.lookup_link",
        side_effect=FileNotFoundError,
    )

    # Mock the LocalStorageManager instantiation to use the mocked database connection
    with app.app_context():  # Set up the application context
        response = client.get("/api/v1/file/non_existent_file")

    assert response.status_code == 404
    assert response.json == {"error": "file not found"}


def test_delete_non_existing_file(client):
    response = client.delete("/api/v1/file/test")
    assert response.status_code == 404
    assert {"error": "file not found"} == response.json


def test_upload_missing_file(client):
    response = client.post("/api/v1/file/test.png")
    assert response.status_code == 400
    assert response.json == {"error": "no file provided"}


def test_upload_file(client, tmpdir):
    # create dummy test file
    p = tmpdir.mkdir("test") / "test.txt"
    p.write("testing body")

    # setup request
    files = {"file": (p.open("rb"),"test.txt")}

    response = client.post(
        "/api/v1/file/test", data=files, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json == {"success": "file uploaded succesfully"}
    # this part is annoying, it hurts me
    os.remove('0/test.txt')
    os.rmdir('0')


def test_file_found(app, client):
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
    app.config["DB"] = db_returns(expected_return)
    response = client.get("/api/v1/file/test.png/info")
    print(response)
    assert response.status_code == 200
    assert expected_return == response.json
