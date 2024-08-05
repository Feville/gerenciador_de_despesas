"""
Módulo que controla as finanças
"""

from datetime import datetime
from typing import Tuple
from flask import jsonify
from pytz import timezone
from core.services.database.finance import FinanceDB


class FinanceController:
    "Gerencia as finanças dos usuários"

    def __init__(self, dao: FinanceDB) -> None:
        self._dao = dao

    def get_user_balance(self, email: str) -> Tuple[jsonify, int]:
        "Obtém o saldo do usuário"
        if not email:
            return jsonify({"msg": "Email não preenchido"}), 400
        response = self._dao.get_balance(email)
        return response

    def get_balance_by_date(self, email: str, date: str) -> Tuple[jsonify, int]:
        "Obtém o saldo do usuário pela data"
        date_parts = date.split("-")
        if len(date_parts) != 2:
            return jsonify({"msg": "Data inválida, deve ser no formato 'YYYY-MM'"}), 400
        year, month = date_parts
        response = self._dao.get_balance_by_date(email, year, month)
        return response

    def add_user_balance(
        self, email: str, amount: float, category_name: str
    ) -> Tuple[jsonify, int]:
        "Adiciona saldo ao usuário na categoria escolhida e grava a data da transação"
        date = (
            datetime.now()
            .astimezone(timezone("America/Sao_Paulo"))
            .strftime("%y-%m-%d %H:%M:%S")
        )
        if amount <= 0:
            return (
                jsonify({"error": "O valor a ser adicionado deve ser positivo."}),
                400,
            )
        response = self._dao.add_user_balance(amount, category_name, email, date)
        return response

    def create_category(self, email: str, category_name: str) -> Tuple[jsonify, int]:
        "Cria categoria"
        if not category_name or not email:
            return jsonify({"msg": "category_name e email são obrigatórios"}), 400
        response = self._dao.create_category(category_name, email)
        return response

    def get_balance_history(self, email: str) -> Tuple[jsonify, int]:
        "Lista os gastos do usuário"
        response = self._dao.get_balance_history(email)
        return response

    def add_loan(
        self, email: str, amount: float, category_name: str
    ) -> Tuple[jsonify, int]:
        "Adiciona empréstimo"
        date = (
            datetime.now()
            .astimezone(timezone("America/Sao_Paulo"))
            .strftime("%y-%m-%d %H:%M:%S")
        )
        if amount <= 0:
            return (
                jsonify({"error": "O valor a ser adicionado deve ser positivo."}),
                400,
            )
        response = self._dao.add_loan(amount, category_name, email, date)
        return response

    def get_loan_history(self, email: str) -> Tuple[jsonify, int]:
        "Histórico de empréstimo"
        response = self._dao.get_loan_history(email)
        return response
