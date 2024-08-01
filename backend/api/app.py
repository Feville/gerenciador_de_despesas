"""
Módulo de aplicação WEB Flask
"""

from flask import Flask
from flask_cors import CORS
from core.logs.logger import setup_logger
from api.routes.access import access_blueprint
from api.routes.finance import finance_blueprint

logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)

app.register_blueprint(access_blueprint)
app.register_blueprint(finance_blueprint)
