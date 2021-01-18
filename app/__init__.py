from flask import Flask
from flask_pymongo import PyMongo

from config import Config

mongo = PyMongo()

def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    mongo.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/fudosan-ai/api')

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    app.register_error_handler(404, not_found)

    return app


def not_found(error):
    return {'error': 'Not found'}, 404
