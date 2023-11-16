import pytest


@pytest.fixture(autouse=True)
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    
    assert b"Hello World!" in response.data
