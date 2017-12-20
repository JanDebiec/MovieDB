import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'userdata/app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#WTF_CSRF_ENABLED = True
#SECRET_KEY = 'you-will-never-guess'
