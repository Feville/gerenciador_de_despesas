"""
Módulo que controla os acessos
"""

import bcrypt
from flask import jsonify, Response
from core.services.database.models.user import User


class AccessController:
    "Gerencia os acessos de usuários"

    def __init__(self, session) -> None:
        self.session = session

    def create_user(self, username, email, password) -> Response:
        "Cria um novo usuário e registra YYYY-MM-DD e H:M:S"
        try:
            hashed_email = bcrypt.hashpw(email.encode("utf-8"), bcrypt.gensalt())
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            new_user = User(
                username=username, email=hashed_email, password=hashed_password
            )
            self.session.add(new_user)
            self.session.commit()
            return jsonify({"msg": "Usuário registrado"}), 201
        except Exception as e:
            self.session.rollback()
            return (
                jsonify(
                    {
                        "msg": "Problema ao registrar usuário, o erro {} ocorreu".format(
                            e
                        )
                    }
                ),
                400,
            )

    def login(self, email, password):
        "Verifica o login do usuário"
        user = self.session.query(User).filter_by(email=email).first()
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return jsonify({"msg": "Usuário logado", "email": email}), 200
        return jsonify({"msg": "Problema ao logar usuário"}), 400
