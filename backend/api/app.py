"""
Módulo de aplicação WEB Flask
"""

from flask import Flask
from flask_cors import CORS
from core.logs.logger import setup_logger


logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)
