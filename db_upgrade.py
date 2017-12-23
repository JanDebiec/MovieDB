#!flask/bin/python
from migrate.versioning import api
# from config import SQLALCHEMY_DATABASE_URI
# from config import SQLALCHEMY_MIGRATE_REPO
from config import Config

api.upgrade(Config.SQLALCHEMY_DATABASE_URI,
            Config.SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(Config.SQLALCHEMY_DATABASE_URI,
                   Config.SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
