"""
Módulo que controla as finanças
"""

from datetime import datetime
from typing import Optional, List, Dict
from pytz import timezone
from sqlalchemy import func, extract
from sqlalchemy.orm import aliased
from core.services.database.database import DatabaseManager
from core.services.database.models.user import Users
from core.services.database.models.categories import Categories
from core.services.database.models.loans import Loans
from core.services.database.models.expenses import Expenses
from api.routes.models.exceptions.finance import ExceptionError


class FinanceController:
    "Gerencia as finanças dos usuários"
    session = DatabaseManager().Session()

    def __init__(self) -> None:
        pass

    def _get_session(self):
        "Inicia a sessão do banco"
        return self.session

    def _get_user_id_by_email(self, email: str) -> dict:
        "Retorna o user_id pelo email do usuário"
        with self._get_session() as session:
            user = session.query(Users).filter_by(email=email).first()
            return {"id": user.id}
        raise ExceptionError("Usuário não encontrado")

    def get_total_amount_expenses(self, user_id: int):
        "Retorna o total de gastos do usuário do banco"
        with self._get_session() as session:
            total_amount = (
                session.query(func.sum(Expenses.amount))
                .filter_by(user_id=user_id)
                .scalar()
            )
            total_amount = total_amount if total_amount is not None else 0
            return total_amount
        raise ExceptionError("Erro ao buscar total de gastos")

    def get_total_amount_expenses_by_date(self, user_id: int, year: str, month: str):
        "Retorna o total de gasto pela data do banco"
        with self._get_session() as session:
            total_amount = (
                session.query(func.sum(Expenses.amount))
                .filter(
                    Expenses.user_id == user_id,
                    extract("year", Expenses.date) == int(year),
                    extract("month", Expenses.date) == int(month),
                )
                .scalar()
            )
            total_amount = total_amount if total_amount is not None else 0
            return total_amount
        raise ExceptionError("Erro ao buscar total de gastos pela data")

    def _verify_date(self, date: str):
        "Formata a data yyyy-mm"
        date_parts = date.split("-")
        if len(date_parts) != 3:
            return date_parts
        _, month, year = date_parts
        return month, year

    def get_category_id_by_name(self, email: str, category_name: str) -> dict:
        "Retorna o category id pelo nome da categoria"
        with self._get_session() as session:
            category = session.query(Categories).filter_by(name=category_name).first()
            if category is None:
                category = self.create_category(email, category_name)
            return {"id": category.id}
        raise ExceptionError("Categoria não encontrada")

    def validate_amount(self, amount: float) -> Optional[int]:
        "Verifica se o número é positivo"
        if amount <= 0:
            return False
        return True

    def verify_category_by_name(self, category_name):
        "Verifica se a categoria existe no banco"
        with self._get_session() as session:
            category = session.query(Categories).filter_by(name=category_name).first()
            if category is not None:
                return False
        return True

    def add_expense_to_db(
        self, user_id: int, category_id: int, amount: float, date: datetime
    ) -> bool:
        "Adiciona gastos do usuário no banco"
        try:
            new_expense = Expenses(
                amount=amount, user_id=user_id, category_id=category_id, date=date
            )
            DatabaseManager().session_insert_data(new_expense)
            return True
        except ExceptionError as e:
            self._get_session().rollback()
            raise ExceptionError(f"Ocorreu um erro ao adicionar o gasto: {e}")

    def add_user_balance(self, email: str, amount: float, category_name: str) -> bool:
        "Adiciona gastos do usuário"
        date = datetime.now().astimezone(timezone("America/Sao_Paulo"))
        self.validate_amount(amount)
        user = self._get_user_id_by_email(email)
        user_id = user["id"]
        category = self.get_category_id_by_name(email, category_name)
        category_id = category["id"]
        self.add_expense_to_db(user_id, category_id, amount, date)
        return True

    def get_user_balance(self, email: str) -> int:
        "Obtém o saldo do usuário"
        user = self._get_user_id_by_email(email)
        user_id = user["id"]
        total_amount = self.get_total_amount_expenses(user_id)
        return total_amount

    def get_balance_by_date(self, email: str, date: str) -> int:
        "Obtém o saldo do usuário pela data"
        year, month = self._verify_date(date)
        user = self._get_user_id_by_email(email)
        user_id = user["id"]
        total_amount = self.get_total_amount_expenses_by_date(user_id, year, month)
        return total_amount

    def create_category(self, email: str, category_name: str) -> Categories:
        "Cria categoria"
        with self._get_session() as session:
            user = self._get_user_id_by_email(email)
            user_id = user["id"]
            new_category = Categories(name=category_name, user_id=user_id)
            session.add(new_category)
            session.commit()
            return new_category

    def get_balance_history(self, email: str) -> dict:
        "Lista os gastos do usuário"
        with self._get_session() as session:
            user = self._get_user_id_by_email(email)
            user_id = user["id"]
            if user_id is None:
                return {"msg": "Usuário não encontrado"}
            category_alias = aliased(Categories)
            expenses = (
                session.query(Expenses, category_alias.name.label("category_name"))
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
        return {"expenses": expense_list}

    def add_loan(self, email: str, amount: float, category_name: str) -> bool:
        "Adiciona um novo empréstimo ao banco de dados"
        loan_date = datetime.now()
        user = self._get_user_id_by_email(email)
        user_id = user["id"]
        if user_id is None:
            return False

        category = self.session.query(Categories).filter_by(name=category_name).first()
        if category is None:
            return False

        new_loan = Loans(
            amount=amount, category_id=category.id, user_id=user_id, date=loan_date
        )
        self.session.add(new_loan)
        self.session.commit()
        return True

    def get_loan_history(self, email: str) -> List[Dict[str, str]]:
        "Obtém o histórico de empréstimos do usuário"
        user = self._get_user_id_by_email(email)
        user_id = user["id"]
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

    def get_categories(self, email: str) -> list:
        "Lista todas as categorias de um usuário"
        user = self._get_user_id_by_email(email)
        user_id = user["id"]
        categories = self.session.query(Categories).filter_by(user_id=user_id).all()
        categories_list = [{"name": category.name} for category in categories]
        return categories_list
