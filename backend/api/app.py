"""
Módulo de aplicação WEB Flask
"""

from flask import Flask
from flask_cors import CORS
from consts import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD
from core.logs.logger import setup_logger
from flask_basicauth import BasicAuth
from flask_httpauth import HTTPBasicAuth


logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)
basic_auth = BasicAuth(app=app)
auth = HTTPBasicAuth()

app.config["BASIC_AUTH_USERNAME"] = BASIC_AUTH_USERNAME
app.config["BASIC_AUTH_PASSWORD"] = BASIC_AUTH_PASSWORD


@auth.verify_password
def verify_password(email, password):
    email = "Biscoito"
    password = "Pastel"
    return email == "Biscoito" and password == "Pastel"
