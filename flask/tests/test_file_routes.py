import pytest
import uuid

from src.app import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_file_not_found(client, mocker):
    # mock the value from get_file
    app.db = mocker.MagicMock()
    response = client.get("/api/v1/file/test")
    assert response.status_code == 404
    assert {"error": "file not found"} == response.json


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
