"""
Módulo que controla os acessos
"""

from core.services.database.access import AccessDB


class AccessController:
    "Gerencia os acessos de usuários"

    def __init__(self, dao: AccessDB) -> None:
        self._dao = dao

    def create_user(self, username, email):
        "Cria um novo usuário e registra YYYY-MM-DD e H:M:S"
        is_register_successfull = self._dao.create_user(username, email)
        if is_register_successfull:
            return {"msg": "Usuário registrado", "user": username}, 201
        return {"msg": "Problema ao registrar usuário"}, 400
