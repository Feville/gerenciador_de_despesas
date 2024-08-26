"""
Módulo que controla os acessos
"""

import bcrypt
from core.services.database.models.user import Users
from core.services.database.database import DatabaseManager


class AccessController:
    "Gerencia os acessos de usuários"

    def __init__(self) -> None:
        self.db_manager = DatabaseManager()

    def _get_session(self):
        "Inicia a sessão do banco"
        return self.db_manager.Session()

    def hash_password(self, password: bytes) -> bytes:
        "Gera o hash da senha"
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password: str, hashed_password: bytes) -> bool:
        "Verifica a senha do usuário comparando com o hash no banco"
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    def build_user(self, username: str, email: str, hashed_password: bytes):
        "Constrói o usuário com os parâmetros necessários"
        if not (username and email and hashed_password):
            return False
        return Users(username=username, email=email, secret_pass=hashed_password)

    def get_user_by_email(self, email: str) -> Users:
        "Pega o usuário pelo email"
        with self._get_session() as session:
            return session.query(Users).filter_by(email=email).first()

    def create_user(self, username: str, email: str, password: str) -> bool:
        "Cria um novo usuário e registra YYYY-MM-DD e H:M:S"
        password_bytes = password.encode("utf-8")
        hashed_password = self.hash_password(password_bytes)
        new_user = self.build_user(username, email, hashed_password)
        create_user = DatabaseManager().session_insert_data(new_user)
        if create_user:
            return True
        return False

    def login(self, email: str, password: str) -> bool:
        "Verifica o login do usuário"
        user = self.get_user_by_email(email)
        if user and self.check_password(password, user.secret_pass):  # type: ignore
            return True
        return False
