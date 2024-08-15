from unittest.mock import patch, MagicMock
import pytest
from core.services.controllers.access import AccessController, Users


@pytest.mark.parametrize(
    "nome, email, senha, expected_email, expected_username, expected_password",
    [
        ("Nome", "email@teste.com", None, "email@teste.com", "Nome", None),
        (
            "OutroNome",
            "outroemail@teste.com",
            "password",
            "outroemail@teste.com",
            "OutroNome",
            "password",
        ),
    ],
)
def test_build_user(
    nome, email, senha, expected_email, expected_username, expected_password
):
    user = AccessController().build_user(nome, email, senha)

    assert isinstance(user, Users)

    assert user.email == expected_email
    assert user.username == expected_username
    assert user.secret_pass == expected_password


@patch("core.services.controllers.access.AccessController.build_user")
def test_build_user_mock(mock_build_user):
    mock_user = MagicMock()
    mock_user.response = {"msg": "Parâmetros incompletos"}
    mock_user.email = "email@teste.com"
    mock_user.username = "Nome"
    mock_user.secret_pass = None
    mock_build_user.response = {"msg": "Parâmetros incompletos"}
    mock_build_user.return_value = mock_user

    user = AccessController().build_user("Nome", "email@teste.com", None)

    assert user.response == {"msg": "Parâmetros incompletos"}
    mock_build_user.assert_called_once_with("Nome", "email@teste.com", None)


@pytest.mark.parametrize(
    "password", ["teste", "senha123", "123456", "umaSenhapoderosa"]
)
def test_hash_password(password):
    hash_password = AccessController().hash_password(password)

    assert isinstance(hash_password, bytes)

    assert hash_password != password

    assert AccessController().check_password(password, hash_password)
