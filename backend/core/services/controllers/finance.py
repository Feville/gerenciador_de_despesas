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
        balance = self._dao.get_balance(email)
        if balance is None:
            self._dao.initialize_balance(email)
            return 0
        return balance

    def add_user_balance(self, email, amount):
        "Adiciona saldo ao usuário"
        if amount <= 0:
            raise ValueError("O valor a ser adicionado deve ser positivo.")
        self._dao.add_balance(email, amount)
        return self.get_user_balance(email)

    def remove_user_balance(self, email, amount):
        "Retira saldo do usuário"
        if amount <= 0:
            raise ValueError("O valor a ser retirado deve ser positivo.")
        current_balance = self.get_user_balance(
            email
        )  # Atualiza o saldo antes de remover
        if current_balance < amount:
            raise ValueError("Saldo insuficiente.")
        self._dao.remove_balance(email, amount)
        return self.get_user_balance(email)
