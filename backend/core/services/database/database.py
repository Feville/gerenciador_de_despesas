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
    """Cria uma tabela no banco de dados"""
    connection = create_connection()
    if connection:
        query = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        );
        """
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            logger.info("Tabela 'user' criada com sucesso")
        except sqlite3.Error as database_error:
            logger.error("O erro '%s' ocorreu", database_error)
        finally:
            connection.close()
