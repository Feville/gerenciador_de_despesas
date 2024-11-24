"""
Rotas de acesso do usuário
"""

from flask import Blueprint, request, jsonify
from core.logs.logger import setup_logger
from core.services.controllers.access import AccessController

logger = setup_logger(__name__)
access_blueprint = Blueprint("access", __name__)

access_controller = AccessController()


@access_blueprint.route("/alive")
def alive():
    "Vê se o servidor está funcionando"
    return "<h1>Alive</h1>"


@access_blueprint.route("/register", methods=["POST"])
def register():
    logger.info("Rota que cadastra usuário")
    data = request.json
    if not data:
        return {"error": "Dados JSON não fornecidos"}, 400
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    response = access_controller.create_user(username, email, password)
    if response:
        return jsonify({"msg": "Problema ao registrar usuário"}), 400
    return jsonify({"msg": "Usuário registrado"}), 201


@access_blueprint.route("/login", methods=["POST"])
def login():
    logger.info("Rota que faz o login dos usuários")
    data = request.json
    if not data:
        return {"error": "Dados JSON não fornecidos"}, 400
    email = data.get("email")
    password = data.get("password")

    response = access_controller.login(email, password)
    if response:
        return jsonify({"msg": "Usuário logado", "email": email}), 200
    return jsonify({"msg": "Problema ao logar usuário:"}), 400
