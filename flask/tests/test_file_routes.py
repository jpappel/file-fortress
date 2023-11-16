import pytest
import uuid
from app import app


@pytest.fixture(autouse=True)
def client():
    
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


    
@pytest.fixture
def mock_file_not_found(mocker):
    get_file_mock = mocker.patch('file.get_file', return_value=None)
    yield get_file_mock

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    
    assert b"Hello World!" in response.data

def test_file_not_found(mocker):
    # mock the get_file function
    mocker.patch('file.get_file', return_value=None)

    response = client.get("/test.png")
    assert response.status_code == 404
    assert {'error': 'file not found'} == response.json

def test_file_found(mocker):
    # mock the get_file function
    mocker.patch('file.get_file', return_value={
        "id": 1,
        "uploader_id": str(uuid.uuid4()),
        "short_link": "test.png",
        "url": "https://example.com/test.png",
        "mime_type": "image/png",
        "expires": None,
        "privacy": "public",
        "modified_date": "2021-01-01 00:00:00",
        "created_date": "2021-01-01 00:00:00"
    })

    response = client.get("/test.png")
    assert response.status_code == 200
    assert {
        "id": 1,
        "uploader_id": mock_file_found.return_value["uploader_id"],
        "short_link": "test.png",
        "url": "https://example.com/test.png",
        "mime_type": "image/png",
        "expires": None,
        "privacy": "public",
        "modified_date": "2021-01-01 00:00:00",
        "created_date": "2021-01-01 00:00:00"
    } == response.json