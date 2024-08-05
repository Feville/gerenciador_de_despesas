"""
Módulo que gerencia o banco de dados de finanças
"""

import sqlite3
from flask import jsonify
from core.logs.logger import setup_logger

logger = setup_logger(__name__)


class FinanceDB:
    "Gerencia as finanças no banco de dados"

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def _create_connection(self):
        return sqlite3.connect(self.db_path)

    def get_user_id_by_email(self, email):
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id_row = cursor.fetchone()
        conn.close()
        if user_id_row:
            return user_id_row[0]
        return None

    def get_balance(self, email):
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400

        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
        total_amount = cursor.fetchone()[0]
        conn.close()

        return (
            jsonify({"balance": total_amount if total_amount is not None else 0}),
            200,
        )

    def get_balance_by_date(self, email, year, month):
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(AMOUNT) FROM expenses WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?",
            (
                user_id,
                year,
                month,
            ),
        )
        total_amount = cursor.fetchone()[0]
        conn.close()

        return (
            jsonify({"balance": total_amount if total_amount is not None else 0}),
            200,
        )

    def add_user_balance(self, amount, category_name, email, date):
        conn = self._create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id_row = cursor.fetchone()
        if user_id_row is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        user_id = user_id_row[0]

        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        category_id_row = cursor.fetchone()
        if category_id_row is None:
            return jsonify({"msg": "Categoria não encontrada"}), 400
        category_id = category_id_row[0]

        cursor.execute(
            "INSERT INTO expenses (amount, category_id, user_id, date) VALUES (?, ?, ?, ?)",
            (amount, category_id, user_id, date),
        )
        conn.commit()
        conn.close()
        return jsonify({"msg": "Despesa adicionada com sucesso"}), 201

    def create_category(self, category_name, email):
        conn = self._create_connection()
        cursor = conn.cursor()

        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400

        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        if cursor.fetchone() is not None:
            return jsonify({"msg": "Categoria já existe"}), 400

        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
        conn.commit()

        return jsonify({"msg": "Categoria criada com sucesso"}), 201

    def add_loan(self, amount, category_name, email, date):
        conn = self._create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id_row = cursor.fetchone()
        if user_id_row is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400
        user_id = user_id_row[0]

        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        category_id_row = cursor.fetchone()
        if category_id_row is None:
            return jsonify({"msg": "Categoria não encontrada"}), 400
        category_id = category_id_row[0]

        cursor.execute(
            "INSERT INTO loans (amount, category_id, user_id, date) VALUES (?, ?, ?, ?)",
            (amount, category_id, user_id, date),
        )
        conn.commit()
        conn.close()
        return jsonify({"msg": "Empréstimo adicionado com sucesso"}), 201

    def get_balance_history(self, email):
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400

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

        return jsonify({"expenses": expense_list}), 200

    def get_loan_history(self, email):
        user_id = self.get_user_id_by_email(email)
        if user_id is None:
            return jsonify({"msg": "Usuário não encontrado"}), 400

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

        return jsonify({"loans": loan_list}), 200
