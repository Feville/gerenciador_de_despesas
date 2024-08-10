"""
Módulo que controla as finanças
"""

from datetime import datetime
from typing import Tuple, Optional, List, Dict
from flask import Response, jsonify
from pytz import timezone
from sqlalchemy import func, extract
from sqlalchemy.orm import aliased
from core.services.database.models.user import Users
from core.services.database.models.categories import Categories
from core.services.database.models.loans import Loans
from core.services.database.models.expenses import Expenses


class FinanceController:
    "Gerencia as finanças dos usuários"

    def __init__(self, session) -> None:
        self.session = session

    def get_user_id_by_email(self, email: str) -> Optional[int]:
        "Retorna o user_id pelo email do usuário"
        # TODO: Refatorar validações
        user = self.session.query(Users).filter_by(email=email).first()
        if user:
            return user.id
        return None

    def get_user_balance(self, email: str) -> Tuple[Response, int]:
        "Obtém o saldo do usuário"
        # TODO: Refatorar validações
        if not email:
            return jsonify({"msg": "Email não preenchido"}), 400
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        total_amount = (
            self.session.query(func.sum(Expenses.amount))
            .filter_by(user_id=user_id)
            .scalar()
        )
        return (
            jsonify({"balance": total_amount if total_amount is not None else 0}),
            200,
        )

    def get_balance_by_date(self, email: str, date: str) -> Tuple[Response, float]:
        "Obtém o saldo do usuário pela data"
        # TODO: Refatorar validações
        date_parts = date.split("-")
        if len(date_parts) != 2:
            return jsonify({"msg": "Data inválida, deve ser no formato 'YYYY-MM'"}), 400
        year, month = date_parts
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        total_amount = (
            self.session.query(func.sum(Expenses.amount))
            .filter(
                Expenses.user_id == user_id,
                extract("year", Expenses.date) == int(year),
                extract("month", Expenses.date) == int(month),
            )
            .scalar()
        )
        return (
            jsonify({"balance": total_amount if total_amount is not None else 0}),
            200,
        )

    def add_user_balance(
        self, email: str, amount: float, category_name: str
    ) -> Tuple[Response, int]:
        # TODO: Refatorar validações
        try:
            "Adiciona saldo ao usuário na categoria escolhida e grava a data da transação"
            date = datetime.now().astimezone(timezone("America/Sao_Paulo"))

            if amount <= 0:
                return (
                    jsonify({"error": "O valor a ser adicionado deve ser positivo."}),
                    400,
                )

            user_id = self.get_user_id_by_email(email)
            if user_id is None:
                return jsonify({"msg": "Usuário não encontrado"}), 400

            category = (
                self.session.query(Categories).filter_by(name=category_name).first()
            )
            if category is None:
                return jsonify({"msg": "Categoria não encontrada"}), 400

            new_expense = Expenses(
                amount=amount, user_id=user_id, category_id=category.id, date=date
            )

            self.session.add(new_expense)
            self.session.commit()
            return jsonify({"msg": "Despesa adicionada com sucesso"}), 201

        except Exception as e:
            self.session.rollback()
            return (
                jsonify({"msg": f"Falha ao adicionar despesa. O erro {e} ocorreu"}),
                500,
            )

    def create_category(self, email: str, category_name: str) -> Tuple[dict, int]:
        "Cria categoria"
        # TODO: Refatorar validações
        try:
            user_id = self.get_user_id_by_email(email)
            if user_id is None:
                return {"msg": "Usuário não encontrado"}, 400

            existing_category = (
                self.session.query(Categories)
                .filter_by(name=category_name)
                .one_or_none()
            )
            if existing_category is not None:
                return {"msg": "Categoria já existe"}, 400

            add_category = Categories(name=category_name, user_id=user_id)
            self.session.add(add_category)
            self.session.commit()

            return {"msg": "Categoria criada com sucesso"}, 201
        except Exception as e:
            return {"msg": f"Falha ao criar categoria. O erro {e} ocorreu"}, 500

    def get_balance_history(self, email: str) -> Tuple[Response, int]:
        "Lista os gastos do usuário"
        # TODO: Refatorar validações
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        category_alias = aliased(Categories)
        expenses = (
            self.session.query(Expenses, category_alias.name.label("category_name"))
            .join(category_alias, Expenses.category_id == category_alias.id)
            .filter(Expenses.user_id == user_id)
            .order_by(Expenses.date.desc())
            .all()
        )
        expense_list = [
            {
                "id": exp[0].id,
                "amount": exp[0].amount,
                "category": exp[1],
                "date": exp[0].date.strftime("%Y-%m-%d"),
            }
            for exp in expenses
        ]
        return jsonify({"expenses": expense_list}), 200

    def add_loan(
        self, amount: float, category_name: str, user_id: int
    ) -> Tuple[Response, int]:
        "Adiciona um novo empréstimo ao banco de dados"
        # TODO: Resolver problema de adicionar loan, categoria nunca é encontrada
        try:
            loan_date = datetime.now()

            category = (
                self.session.query(Categories)
                .filter_by(name=category_name)
                .one_or_none()
            )
            if category is None:
                return jsonify({"error": "Categoria não encontrada."}), 404

            new_loan = Loans(
                amount=amount, category_id=category.id, user_id=user_id, date=loan_date
            )

            self.session.add(new_loan)
            self.session.commit()

            return jsonify({"msg": "Empréstimo adicionado com sucesso."}), 201

        except Exception as e:
            self.session.rollback()
            return (
                jsonify(
                    {"error": f"Falha ao adicionar empréstimo. O erro {e} ocorreu."}
                ),
                500,
            )

    def get_loan_history(self, user_id: int) -> List[Dict[str, any]]:
        "Obtém o histórico de empréstimos do usuário"
        # TODO: Refatorar validações
        category_alias = aliased(Categories)

        loans = (
            self.session.query(Loans, category_alias.name.label("category_name"))
            .join(category_alias, Loans.category_id == category_alias.id)
            .filter(Loans.user_id == user_id)
            .order_by(Loans.date.desc())
            .all()
        )

        loan_list = [
            {
                "id": loan[0].id,
                "amount": loan[0].amount,
                "category": loan[1],
                "date": loan[0].date.strftime("%Y-%m-%d"),
            }
            for loan in loans
        ]

        return loan_list
