"""
Rotas de finanças do usuário
"""

from flask import Blueprint, request
from core.logs.logger import setup_logger
from core.services.controllers.finance import FinanceController
from core.services.database.finance import FinanceDB

logger = setup_logger(__name__)
finance_blueprint = Blueprint("finance", __name__)

dao = FinanceDB()
finance_controller = FinanceController(dao)


@finance_blueprint.route("/get_balance", methods=["GET"])
def get_balance():
    logger.info("Rota que mostra o saldo do usuário")
    data = request.args
    email = data.get("email")

    response = finance_controller.get_user_balance(email)
    return response


@finance_blueprint.route("/get_balance_by_date", methods=["GET"])
def get_balance_by_date():
    logger.info("Rota que mostra o saldo do usuário pela data")
    data = request.args
    email = data.get("email")
    date = data.get("date")

    response = finance_controller.get_balance_by_date(email, date)
    return response


@finance_blueprint.route("/add_user_balance", methods=["POST"])
def add_user_balance():
    logger.info("Rota que adiciona saldo e categoria do gasto do usuário")
    data = request.json
    email = data.get("email")
    amount = data.get("amount")
    category_name = data.get("category_name")

    response = finance_controller.add_user_balance(email, amount, category_name)
    return response


@finance_blueprint.route("/create_category", methods=["POST"])
def create_category():
    logger.info("Rota que cria categorias")
    data = request.json
    email = data.get("email")
    category_name = data.get("category_name")

    response = finance_controller.create_category(email, category_name)
    return response


@finance_blueprint.route("/get_balance_history", methods=["GET"])
def get_balance_history():
    logger.info("Rota que lista os gastos do usuário")
    data = request.args
    email = data.get("email")

    response = finance_controller.get_balance_history(email)
    return response
