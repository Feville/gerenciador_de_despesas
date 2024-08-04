"""
Módulo que gerencia os acessos dos usuários
"""

import sqlite3


class AccessDB:
    "Inicia banco do usuário"

    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def create_user(self, username, email, hashed_password):
        "Adiciona um usuário novo no banco"
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            connection.close()
            return False

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password),
        )
        connection.commit()
        connection.close()
        return True

    def get_user_by_email(self, email):
        "Recupera o usuário pelo email"
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        connection.close()
        if result:
            return {"password": result[0]}
        return None
