import sqlite3


class FinanceDB:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._create_connection()

    def _create_connection(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def _close_connection(self):
        self.conn.commit()
        self.conn.close()

    def setup_for_testing(self):
        """Método público para configurar o banco de dados em testes"""
        self._create_connection()
        self._check_and_create_balance_column()

    def teardown_for_testing(self):
        """Método público para fechar a conexão após testes"""
        self._close_connection()

    def _check_and_create_balance_column(self):
        self.cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in self.cursor.fetchall()]
        if "saldo" not in columns:
            self.cursor.execute("ALTER TABLE user ADD COLUMN saldo REAL DEFAULT 0")
            self.conn.commit()

    def get_balance(self, email):
        self._check_and_create_balance_column()
        self.cursor.execute("SELECT saldo FROM user WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        if result is None:
            return 0
        return result[0]

    def add_balance(self, email, amount):
        self._check_and_create_balance_column()
        current_balance = self.get_balance(email)
        new_balance = current_balance + amount
        self.cursor.execute(
            "UPDATE user SET saldo = ? WHERE email = ?", (new_balance, email)
        )
        self.conn.commit()

    def remove_balance(self, email, amount):
        self._check_and_create_balance_column()
        current_balance = self.get_balance(email)
        new_balance = current_balance - amount
        self.cursor.execute(
            "UPDATE user SET saldo = ? WHERE email = ?", (new_balance, email)
        )
        self.conn.commit()
