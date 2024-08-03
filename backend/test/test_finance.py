import shutil
import os
from test.test_config import create_test_app
import pytest
from core.services.controllers.finance import FinanceController
from core.services.database.finance import FinanceDB


@pytest.fixture
def setup_db():
    original_db_path = "database.db"
    test_db_path = "test_database.db"
    shutil.copyfile(original_db_path, test_db_path)

    db = FinanceDB(test_db_path)

    yield db

    os.remove(test_db_path)


@pytest.fixture
def test_client():
    app = create_test_app()
    return app.test_client()


@pytest.fixture
def mock_finance_controller(setup_db):
    return FinanceController(setup_db)


def test_add_user_balance_success(test_client, mock_finance_controller):
    email = "teste@email.com"
    initial_amount = mock_finance_controller.get_user_balance(email)
    additional_amount = 1
    expected_balance = initial_amount + additional_amount

    response = test_client.post(
        "/add_user_balance",
        json={"email": email, "amount": additional_amount},
    )

    print("Response Data:", response.data)
    print("Response JSON:", response.get_json())

    assert response.status_code == 200
    assert response.get_json() == {"Balance": expected_balance}
