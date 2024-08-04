# backend/test/test_config.py
from flask import Flask
from api.router import register_routes


def create_test_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    register_routes(app)
    return app
