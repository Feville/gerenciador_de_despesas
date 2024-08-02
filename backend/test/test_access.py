from unittest.mock import MagicMock
import pytest
from core.services.controllers.access import AccessController
from .test_config import create_test_app


@pytest.fixture
def app():
    return create_test_app()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_access_controller():
    mock_controller = MagicMock(spec=AccessController)
    return mock_controller


def test_alive(client):
    """Testa a rota /alive"""
    response = client.get("/alive")
    assert response.status_code == 200
    assert b"<h1>Alive</h1>" in response.data


def test_register_success(client, mock_access_controller):
    """Testa a rota /register com dados válidos"""
    mock_access_controller.create_user.return_value = {"message": "User created"}, 201
    AccessController.create_user = mock_access_controller.create_user

    response = client.post(
        "/register", json={"username": "testuser", "email": "testuser@example.com"}
    )

    assert response.status_code == 200
    assert response.json == {"message": "User created"}


def test_register_failure(client, mock_access_controller):
    """Testa a rota /register com dados inválidos"""
    mock_access_controller.create_user.return_value = {"message": "Invalid data"}, 400
    AccessController.create_user = mock_access_controller.create_user

    response = client.post("/register", json={"username": "", "email": ""})

    assert response.status_code == 400
    assert response.json == {"message": "Invalid data"}
