import sqlite3


def create_connection():
    """Cria e retorna uma conexão com o banco de dados"""
    connection = None
    connection = sqlite3.connect("database.db")
    return connection


def create_table():
    """Cria uma tabela no banco de dados"""
    connection = create_connection()
    if connection:
        query = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            saldo REAL DEFAULT 0
        );
        """
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()


create_table()
