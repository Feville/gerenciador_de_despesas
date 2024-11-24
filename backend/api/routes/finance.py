"""
Rotas de finanças do usuário
"""

from flask import Blueprint, request, jsonify
from core.logs.logger import setup_logger
from core.services.controllers.finance import FinanceController
from api.routes.models.exceptions.finance import ExceptionError

logger = setup_logger(__name__)
finance_blueprint = Blueprint("finance", __name__, url_prefix="/api/v1")

finance_controller = FinanceController()


@finance_blueprint.errorhandler(ExceptionError)
def errorHandler(e):
    return jsonify({"error": str(e)}), 400


@finance_blueprint.route("/get_balance/<email>", methods=["GET"])
def get_balance(email: str):
    logger.info("Rota que mostra o saldo do usuário")
    response = finance_controller.get_user_balance(email)
    if response:
        return jsonify({"total_amount": response}), 200
    return jsonify({"msg": response}), 400


@finance_blueprint.route("/get_balance_by_date/<email>/<date>", methods=["GET"])
def get_balance_by_date(email: str, date: str):
    logger.info("Rota que mostra o saldo do usuário pela data")
    total_amount = finance_controller.get_balance_by_date(email, date)
    return jsonify({"total_amount": total_amount})


@finance_blueprint.route("/add_user_balance", methods=["POST"])
def add_user_balance():
    logger.info("Rota que adiciona saldo e categoria do gasto do usuário")
    data = request.json
    if data is None:
        return {"error": "Dados JSON não fornecidos"}, 400
    email = data.get("email")
    amount = data.get("amount")
    category_name = data.get("category_name")

    response = finance_controller.add_user_balance(email, amount, category_name)
    if response:
        return jsonify({"msg": "Despesa adicionada com sucesso"}), 201
    return jsonify({"msg": "Erro ao adicionar despesa"}), 400


@finance_blueprint.route("/create_category", methods=["POST"])
def create_category():
    logger.info("Rota que cria categorias")
    data = request.json
    if data is None:
        return {"error": "Dados JSON não fornecidos"}, 400
    email = data.get("email")
    category_name = data.get("category_name")

    response = finance_controller.create_category(email, category_name)
    if response:
        return jsonify({"msg": "Adicionado com sucesso"}), 200
    return jsonify({"msg": "Categoria não pode ser criada"}), 400


@finance_blueprint.route("/get_balance_history/<email>", methods=["GET"])
def get_balance_history(email: str):
    logger.info("Rota que lista os gastos do usuário")
    response = finance_controller.get_balance_history(email)
    return jsonify(response)


@finance_blueprint.route("/add_loan", methods=["POST"])
def add_loan():
    logger.info("Rota que adiciona empréstimo")
    data = request.json
    if data is None:
        return {"error": "Dados JSON não fornecidos"}, 400
    email = data.get("email")
    amount = data.get("amount")
    category_name = data.get("category_name")

    response = finance_controller.add_loan(email, amount, category_name)
    if response:
        return jsonify({"msg": "Empréstimo adicionado com sucesso."}), 201
    return {"msg": "Usuário não encontrado"}, 400


@finance_blueprint.route("/get_loan_history/<email>", methods=["GET"])
def get_loan_history(email: str):
    logger.info("Rota que mostra o histórico de empréstimos")
    response = finance_controller.get_loan_history(email)
    return jsonify({"msg": response}), 200


@finance_blueprint.route("/get_categories/<email>", methods=["GET"])
def get_history(email: str):
    logger.info("Rota que mostra todas as categorias")
    response = finance_controller.get_categories(email)
    return jsonify({"msg": response}), 200
