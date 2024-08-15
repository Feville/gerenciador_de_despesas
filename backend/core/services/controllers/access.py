"""
Módulo que controla os acessos
"""

import bcrypt
from flask import jsonify, Response
from core.services.database.models.user import Users
from core.services.database.database import DatabaseManager


class AccessController:
    "Gerencia os acessos de usuários"

    def __init__(self) -> None:
        self.db_manager = DatabaseManager()

    def _get_session(self):
        "Inicia a sessão do banco"
        session = self.db_manager.Session()
        return session

    def hash_password(self, password: str):
        "Coloca o hash na senha do usuário"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password

    def check_password(self, password: str, hashed_password: str):
        "Verifica a senha do usuário comparando com o hash no banco"
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return True
        return False

    def handle_commit_error(self, e: Exception) -> Response:
        "Erro de envio"
        session = self._get_session()
        session.rollback()
        return (
            jsonify({"msg": f"Problema ao registrar usuário, o erro {e} ocorreu"}),
            400,
        )

    def build_user(self, username: str, email: str, hashed_password: str):
        if (username or email or hashed_password) is None:
            return False
        return Users(username=username, email=email, secret_pass=hashed_password)

    def get_user_by_email(self, email: str) -> Users:
        return self.db_manager.Session.query(Users).filter_by(email=email).first()

    def create_user(self, username, email, password) -> Response:
        "Cria um novo usuário e registra YYYY-MM-DD e H:M:S"
        try:
            hashed_password = self.hash_password(password)
            new_user = self.build_user(username, email, hashed_password)
            if new_user is False:
                return jsonify({"msg": "Parâmetros incompletos"}), 404
            self._get_session().add(new_user)
            self._get_session().commit()
            return jsonify({"msg": "Usuário registrado"}), 201
        except Exception as e:
            session = self._get_session()
            session.rollback()
            return self.handle_commit_error(e)

    def login(self, email: str, password: str) -> Response:
        "Verifica o login do usuário"
        user = self.get_user_by_email(email)
        if user and self.check_password(password, user.secret_pass):
            return jsonify({"msg": "Usuário logado", "email": email}), 200
        return jsonify({"msg": "Problema ao logar usuário"}), 400
