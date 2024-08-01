"""
Módulo de aplicação WEB Flask
"""

from flask import Flask
from flask_cors import CORS
from core.logs.logger import setup_logger
from api.routes.access import access_blueprint

logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)


def create_app() -> Flask:

    app.register_blueprint(access_blueprint)

    return app
