from flask import Flask
from flask_restful import Api
from app.config import Config
from app.commands import init_db_command
from app.extensions import db, migrate
from app.resource import UrlResource


COMMANDS = [init_db_command]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_commands(app)
    register_extensions(app)
    register_api(app)

    return app


def register_api(app):
    api = Api(app)
    api.add_resource(UrlResource, '/', '/<string:short_url>')


def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)


def register_commands(app):

    for command in COMMANDS:
        app.cli.add_command(command)
