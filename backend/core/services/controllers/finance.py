"""
Módulo que controla as finanças
"""

from core.services.database.finance import FinanceDB


class FinanceController:
    "Gerencia as finanças dos usuários"

    def __init__(self, dao: FinanceDB) -> None:
        self._dao = dao

    def get_user_balance(self, email):
        "Obtém o saldo do usuário"
        return self._dao.get_balance(email)

    def add_user_balance(self, email, amount):
        "Adiciona saldo ao usuário"
        if amount <= 0:
            raise ValueError("O valor a ser adicionado deve ser positivo.")
        self._dao.add_balance(email, amount)
        return self.get_user_balance(email)

    def remove_user_balance(self, email, amount):
        "Retira saldo do usuário"
        if amount <= 0:
            raise ValueError("O valor a ser retirado deve ser positivo")
        self._dao.remove_balance(email)
