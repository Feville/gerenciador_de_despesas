"""
Módulo que gerencia o usuário no banco de dados
"""

import sqlite3


class AccessDB:
    "Inicia banco do usuário"

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def create_user(self, username, email):
        "Adiciona um usuário novo no banco"
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            return False

        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email),
        )
        connection.commit()
        connection.close()
        return True

    def check_login(self, username, email):
        "Verifica se o login da pessoa existe no banco"
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND email = ?",
            (username, email),
        )
        user = cursor.fetchone()
        connection.close()
        return user
