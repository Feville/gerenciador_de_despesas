"""
Rotas de finanças do usuário
"""

from flask import Blueprint, request, jsonify
from core.logs.logger import setup_logger
from core.services.controllers.finance import FinanceController
from core.services.database.finance import FinanceDB

logger = setup_logger(__name__)
finance_blueprint = Blueprint("finance", __name__)

dao = FinanceDB()
finance_controller = FinanceController(dao)


@finance_blueprint.route("/add_cash", methods=["POST"])
def add_cash():
    data = request.json
    email = data.get("email")
    amount = data.get("amount")

    response = finance_controller.add_user_balance(email, amount)
    return jsonify(response)


@finance_blueprint.route("/get_balance", methods=["GET"])
def get_balance():
    data = request.json
    email = data.get("email")

    response = finance_controller.get_user_balance(email)
    return jsonify(response)
