from flask import Flask
from flask_restful import Api
from app.config import Config
from app.commands import add_admin_command, init_db_command
from app.extensions import db, migrate, jwt
from app.resource.auth import UserResource, LoginResource
# from app.resource.url_shortener import UrlResource


COMMANDS = [init_db_command, add_admin_command]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_commands(app)
    register_extensions(app)
    register_api(app)

    return app


def register_api(app):
    api = Api(app)
    api.add_resource(UserResource, '/register')
    api.add_resource(LoginResource, '/login')
    # api.add_resource(UserResource, '/pico/<changed>', '/change')


def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-JWT-Extended
    jwt.init_app(app)


def register_commands(app):

    for command in COMMANDS:
        app.cli.add_command(command)
