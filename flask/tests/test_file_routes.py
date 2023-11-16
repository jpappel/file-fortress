import pytest
import uuid

from src.app import app

@pytest.fixture()
def client():
    
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_file_not_found(client,mocker):
    # mock the value from get_file
    mocked_get_file = mocker.patch('src.file_routes.get_file')
    mocked_get_file.return_value = None

    response = client.get("/api/v1/file/test.png")
    assert response.status_code == 404
    assert {'error': 'file not found'} == response.json

def test_file_found(client, mocker):
    #mock the value from get_file
    mocked_get_file = mocker.patch('src.file_routes.get_file')
    expected_return = {
        "id": 1,
        "uploader_id": str(uuid.uuid4()),
        "short_link": "test.png",
        "url": "https://example.com/test.png",
        "mime_type": "image/png",
        "expires": None,
        "privacy": "public",
        "modified_date": "2021-01-01 00:00:00",
        "created_date": "2021-01-01 00:00:00"
    }

    mocked_get_file.return_value = expected_return
    response = client.get("/api/v1/file/test.png")
    assert response.status_code == 200
    assert expected_return == response.json