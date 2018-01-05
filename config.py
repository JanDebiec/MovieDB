import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'userdata/app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    MOVIES_PER_PAGE = 25

