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
        return self.db_manager.Session()

    def hash_password(self, password: str) -> str:
        "Gera o hash da senha"
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str, hashed_password: str) -> bool:
        "Verifica a senha do usuário comparando com o hash no banco"
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    def handle_commit_error_user_exist(self) -> Response:
        "Erro de envio"
        return jsonify({"msg": "Usuário já existe"}), 400

    def build_user(self, username: str, email: str, hashed_password: bytes):
        if not (username and email and hashed_password):
            return False
        return Users(username=username, email=email, secret_pass=hashed_password)

    def get_user_by_email(self, email: str) -> Users:
        with self._get_session() as session:
            return session.query(Users).filter_by(email=email).first()

    def create_user(self, username, email, password) -> Response:
        "Cria um novo usuário e registra YYYY-MM-DD e H:M:S"
        try:
            hashed_password = self.hash_password(password)
            new_user = self.build_user(username, email, hashed_password)
            if not new_user:
                return jsonify({"msg": "Parâmetros incompletos"}), 404
            with self._get_session() as session:
                session.add(new_user)
                session.commit()
            return jsonify({"msg": "Usuário registrado"}), 201
        except Exception:
            session = self._get_session()
            session.rollback()
            return self.handle_commit_error_user_exist()

    def login(self, email: str, password: str) -> Response:
        "Verifica o login do usuário"
        try:
            user = self.get_user_by_email(email)
            if user and self.check_password(password, user.secret_pass):
                return jsonify({"msg": "Usuário logado", "email": email}), 200
            else:
                return jsonify({"msg": "Credenciais inválidas"}), 401
        except Exception:
            return jsonify({"msg": "Problema ao logar usuário:"}), 400
