import pytest
from flask import Flask
from src import create_app

from src.configurations import TestConfig
from src.website_routes import website


@pytest.fixture
def app():
    app = Flask(__name__, template_folder='../src/templates')
    app.config["TESTING"] = True
    app.register_blueprint(website)
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == open('../src/templates/index.html', 'rb').read().strip()
