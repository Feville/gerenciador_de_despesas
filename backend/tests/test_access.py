import pytest
from core.services.controllers.access import AccessController, Users


@pytest.mark.parametrize(
    "nome, email, senha, expected_email, expected_username, expected_password",
    [
        (
            "Nome",
            "email@teste.com",
            "hashed_password",
            "email@teste.com",
            "Nome",
            "hashed_password",
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


@pytest.mark.parametrize(
    "password", ["teste", "senha123", "123456", "umaSenhapoderosa"]
)
def test_hash_password(password):
    hash_password = AccessController().hash_password(password)

    assert isinstance(hash_password, bytes)

    assert hash_password != password

    check_password = AccessController().check_password(password, hash_password)

    assert isinstance(check_password, bool)
