"""
Módulo que controla as finanças
"""

from datetime import datetime
from typing import Tuple
from flask import Response, jsonify, Optional
from pytz import timezone
from core.services.database.finance import FinanceDB


class FinanceController:
    "Gerencia as finanças dos usuários"

    def __init__(self, dao: FinanceDB) -> None:
        self._dao = dao

    def get_user_id_by_email(self, email: str) -> Optional[int]:
        user_id = self._dao.get_user_id_by_email(email)
        return user_id

    def get_user_balance(self, email: str) -> Tuple[Response, int]:
        "Obtém o saldo do usuário"
        if not email:
            return jsonify({"msg": "Email não preenchido"}), 400
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        total_amount = self._dao.get_user_balance(user_id)
        return (
            jsonify({"balance": total_amount if total_amount is not None else 0}),
            200,
        )

    def get_balance_by_date(self, email: str, date: str) -> Tuple[Response, int]:
        "Obtém o saldo do usuário pela data"
        date_parts = date.split("-")
        if len(date_parts) != 2:
            return jsonify({"msg": "Data inválida, deve ser no formato 'YYYY-MM'"}), 400
        year, month = date_parts
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        total_amount = self._dao.get_balance_by_date(user_id, year, month)
        return (
            jsonify({"balance": total_amount if total_amount is not None else 0}),
            200,
        )

    def add_user_balance(
        self, email: str, amount: float, category_name: str
    ) -> Tuple[Response, str]:
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
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        balance = self._dao.add_user_balance(amount, category_name, user_id, date)
        if balance is None:
            return jsonify({"msg": "Categoria não encontrada"}), 400
        return jsonify({"msg": "Despesa adicionada com sucesso"}), 201

    def create_category(self, email: str, category_name: str) -> Tuple[list, int]:
        "Cria categoria"
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        response = self._dao.create_category(category_name)
        if response is False:
            return jsonify({"msg": "Categoria já existe"}), 400
        return jsonify({"msg": "Categoria criada com sucesso"}), 201

    def get_balance_history(self, email: str) -> Tuple[Response, int]:
        "Lista os gastos do usuário"
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        expense_list = self._dao.get_balance_history(user_id)
        return jsonify({"expenses": expense_list}), 200

    def add_loan(
        self, email: str, amount: float, category_name: str
    ) -> Tuple[Response, int]:
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
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        response = self._dao.add_loan(amount, category_name, user_id, date)
        if response is False:
            return jsonify({"msg": "Categoria não encontrada"}), 400
        return jsonify({"msg": "Empréstimo adicionado com sucesso"}), 201

    def get_loan_history(self, email: str) -> Tuple[Response, int]:
        "Histórico de empréstimo"
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        loan_list = self._dao.get_loan_history(user_id)
        return jsonify({"loans": loan_list}), 200
