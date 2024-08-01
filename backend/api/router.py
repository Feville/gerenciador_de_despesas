"""
Módulo que cria as rotas no Flask
"""

from flask import Flask
from api.routes.access import access_blueprint
from api.routes.finance import finance_blueprint


def register_routes(app: Flask):
    "Registra rotas no flask"
    app.register_blueprint(access_blueprint)
    app.register_blueprint(finance_blueprint)
