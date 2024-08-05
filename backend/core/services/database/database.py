"""
Módulo que fornece funções para criar uma conexão com um banco de dados
"""

import sqlite3
from core.logs.logger import setup_logger

logger = setup_logger(__name__)


def create_connection():
    """Cria e retorna uma conexão com o banco de dados"""
    connection = None
    try:
        connection = sqlite3.connect("database.db")
        logger.info("Conexão com o banco criada com sucesso")
    except sqlite3.Error as database_error:
        logger.error(
            "Ocorreu um erro ao conectar ao banco de dados: %s", database_error
        )
    return connection


def create_table():
    """Cria as tabelas no banco de dados"""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                );
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category_id INTEGER,
                    user_id INTEGER,
                    date DATE NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category_id INTEGER,
                    user_id INTEGER,
                    date DATE NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """
            )

            connection.commit()
            logger.info("Tabelas criadas com sucesso")
        except sqlite3.Error as database_error:
            logger.error("O erro '%s' ocorreu", database_error)
        finally:
            connection.close()
