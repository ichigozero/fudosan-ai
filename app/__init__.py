from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    return app