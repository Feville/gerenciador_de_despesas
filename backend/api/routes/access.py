"""
Rotas de acesso do usuário
"""

from flask import Blueprint, request, jsonify
from core.logs.logger import setup_logger
from core.services.controllers.access import AccessController
from core.services.database.access import (
    AccessDB,
)

logger = setup_logger(__name__)
access_blueprint = Blueprint("access", __name__)


dao = AccessDB()
access_controller = AccessController(dao)


@access_blueprint.route("/alive")
def alive():
    "Vê se o servidor está funcionando"
    return "<h1>Alive</h1>"


@access_blueprint.route("/register", methods=["POST"])
def register():
    logger.info("Rota que cadastra usuário")
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    response, status_code = access_controller.create_user(username, email, password)

    if status_code == 201:
        return jsonify(response), 200
    return jsonify(response), 400


@access_blueprint.route("/login", methods=["POST"])
def login():
    logger.info("Rota que faz o login dos usuários")
    data = request.json
    email = data.get("email")
    password = data.get("password")

    response = access_controller.login(email, password)
    return response
