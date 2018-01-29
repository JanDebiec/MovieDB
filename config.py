import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'userdata/app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # the next setting is not used with: flask db migrate
    # only for old methode: with files: db_migrate, db_upgrate.
    # but old method was not functioning on 29.01.18. The new method was OK
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    MOVIES_PER_PAGE = 25

    OWNER_NAME = 'JD'

    MAX_VAL_NORM = 100
