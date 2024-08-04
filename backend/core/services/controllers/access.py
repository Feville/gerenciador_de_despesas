"""
Módulo que controla os acessos
"""

import bcrypt
from core.services.database.access import AccessDB


class AccessController:
    "Gerencia os acessos de usuários"

    def __init__(self, dao: AccessDB) -> None:
        self._dao = dao

    def create_user(self, username, email, password):
        "Cria um novo usuário e registra YYYY-MM-DD e H:M:S"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        is_register_successfull = self._dao.create_user(
            username, email, hashed_password
        )
        if is_register_successfull:
            return {"msg": "Usuário registrado", "user": username}, 201
        return {"msg": "Problema ao registrar usuário"}, 400

    def login(self, email, password):
        "Verifica o login do usuário"
        user = self._dao.get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return {"msg": "Usuário logado", "email": email}, 200
        return {"msg": "Problema ao logar usuário"}, 400
