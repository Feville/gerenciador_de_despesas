"""
Módulo que gerencia o banco de dados de finanças
"""

import sqlite3
from typing import Optional, Tuple, List, Dict
from flask import jsonify
from core.logs.logger import setup_logger

logger = setup_logger(__name__)


class FinanceDB:
    "Gerencia as finanças no banco de dados"

    def __init__(self, db_path: str = "database.db") -> None:
        self.db_path = db_path

    def _create_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_user_id_by_email(self, email: str) -> Optional[int]:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id_row = cursor.fetchone()
        conn.close()
        if user_id_row:
            return user_id_row[0]
        return None

    def get_user_balance(self, user_id: int) -> Optional[float]:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        total_amount = cursor.fetchone()[0]
        conn.close()
        return total_amount

    def get_balance_by_date(
        self, user_id: int, year: str, month: str
    ) -> Optional[float]:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?",
            (user_id, year, month),
        )
        total_amount = cursor.fetchone()[0]
        conn.close()
        return total_amount

    def add_user_balance(
        self, amount: float, category_name: str, user_id: int, date: str
    ) -> Optional[bool]:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        if cursor.fetchone() is not None:
            return False
        category_id_row = cursor.fetchone()
        category_id = category_id_row[0]
        cursor.execute(
            "INSERT INTO expenses (amount, category_id, user_id, date) VALUES (?, ?, ?, ?)",
            (amount, category_id, user_id, date),
        )
        conn.commit()
        conn.close()
        return True

    def create_category(self, category_name: str) -> Optional[bool]:
        conn = self._create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        if cursor.fetchone() is not None:
            return False
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
        conn.commit()
        return True

    def add_loan(
        self, amount: float, category_name: str, user_id: str, date: str
    ) -> bool:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        category_id_row = cursor.fetchone()
        if category_id_row is None:
            return False
        category_id = category_id_row[0]

        cursor.execute(
            "INSERT INTO loans (amount, category_id, user_id, date) VALUES (?, ?, ?, ?)",
            (amount, category_id, user_id, date),
        )
        conn.commit()
        conn.close()
        return True

    def get_balance_history(self, user_id: int) -> List[Dict[str, any]]:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.id, e.amount, c.name as category, e.date
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = ?
            ORDER BY e.date DESC
            """,
            (user_id,),
        )
        expenses = cursor.fetchall()
        conn.close()

        expense_list = [
            {"id": exp[0], "amount": exp[1], "category": exp[2], "date": exp[3]}
            for exp in expenses
        ]

        return expense_list

    def get_loan_history(self, user_id: int) -> List[Dict[str, any]]:
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT l.id, l.amount, c.name as category, l.date
            FROM loans l
            JOIN categories c ON l.category_id = c.id
            WHERE l.user_id = ?
            ORDER BY l.date DESC
            """,
            (user_id,),
        )
        loans = cursor.fetchall()
        conn.close()

        loan_list = [
            {"id": loan[0], "amount": loan[1], "category": loan[2], "date": loan[3]}
            for loan in loans
        ]

        return loan_list
