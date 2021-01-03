from flask import Flask
from flask_pymongo import PyMongo

from config import Config

mongo = PyMongo()

def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    mongo.init_app(app)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    return app