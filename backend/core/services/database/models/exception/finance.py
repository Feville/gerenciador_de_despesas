""" Módulo que representa as categorias de despesas"""

from flask import jsonify


class FinanceException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_response(self):
        return jsonify({"msg": self.message}), self.status_code
