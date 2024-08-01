"""
Módulo que cria as rotas no Flask
"""

from flask import Flask
from api.routes.access import access_blueprint


def register_routes(app: Flask):
    "Registra rotas no flask"
    app.register_blueprint(access_blueprint)
