import os
import shutil
from test.test_config import create_test_app
import pytest
from core.services.controllers.finance import FinanceController
from core.services.database.finance import FinanceDB


@pytest.fixture
def test_client():
    app = create_test_app()
    with app.app_context():
        yield app.test_client()


@pytest.fixture
def setup_db():
    original_db_path = "database.db"
    test_db_path = "test_database.db"
    shutil.copyfile(original_db_path, test_db_path)

    db = FinanceDB(test_db_path)

    yield db

    os.remove(test_db_path)


@pytest.fixture
def mock_finance_controller(setup_db):
    # Certifique-se de que o contexto da aplicação está ativo
    app = create_test_app()
    with app.app_context():
        return FinanceController(setup_db)


def test_get_user_balance_success(test_client, mock_finance_controller):
    email = "teste@email.com"
    category_name = "Comida"

    # Obtém a resposta da função get_user_balance
    response = mock_finance_controller.get_user_balance(email)

    # Se a função get_user_balance retornar uma Response, extraia o valor do conteúdo
    if isinstance(response, dict):
        initial_amount = response.get("Balance", 0)
    else:
        # Trate casos onde response pode não ser um dicionário
        initial_amount = 0

    additional_amount = (
        50  # Este valor deve ser configurado de acordo com o cenário de teste
    )
    # Adiciona um saldo para o teste
    mock_finance_controller.add_user_balance(email, additional_amount, category_name)

    expected_balance = initial_amount + additional_amount

    response = test_client.get(
        "/get_balance",
        query_string={"email": email},
    )

    assert response.status_code == 200
    assert response.get_json() == {"balance": expected_balance}
