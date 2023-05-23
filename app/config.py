import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    PROJECT_NAME = "flask_microblog"
    PROJECT_ROOT = PROJECT_ROOT
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')
    SECRET_KEY = 'asd;lkajs-90 as;doaks/A'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
