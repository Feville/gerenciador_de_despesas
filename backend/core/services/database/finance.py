"""
Módulo que gerencia o banco de dados de finanças
"""

import sqlite3


class FinanceDB:
    "Gerencia a persistência das finanças no banco de dados"

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def _create_connection(self):
        return sqlite3.connect(self.db_path)

    def get_balance(self, email):
        "Obtém o saldo do usuário"
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(user);")
        cursor.execute("SELECT saldo FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None

    def add_balance(self, email, amount, date):
        "Adiciona saldo ao usuário"
        connection = self._create_connection()
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]

        if "date" not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN date TEXT")

        cursor.execute(
            "UPDATE user SET saldo = saldo + ?, date = ? WHERE email = ?",
            (amount, date, email),
        )

        connection.commit()
        connection.close()

    def remove_balance(self, email, amount):
        "Remove saldo do usuário"
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE user SET saldo = saldo - ? WHERE email = ?", (amount, email)
        )
        connection.commit()
        connection.close()

    def initialize_balance(self, email):
        "Inicializa o saldo do usuário como 0 se não existir"
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE user SET saldo = 0 WHERE email = ?", (email,))
        connection.commit()
        connection.close()
