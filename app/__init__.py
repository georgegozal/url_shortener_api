from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import Config
from app.commands import init_db_command
from app.extensions import db
from app.resource import UrlResource


COMMANDS = [init_db_command]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_commands(app)
    register_extensions(app)
    register_api(app)
    register_swagger(app)
    return app


def register_api(app):
    api = Api(app)
    api.add_resource(UrlResource, '/api/url/', '/api/url/<string:short_url>')


def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

def register_commands(app):

    for command in COMMANDS:
        app.cli.add_command(command)

def register_swagger(app):
    SWAGGER_URL = ''
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "url shortener"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)