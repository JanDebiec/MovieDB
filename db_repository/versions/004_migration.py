from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('movie_id', Integer),
    Column('characterName', String(length=64)),
)

movie = Table('movie', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('imdbId', VARCHAR(length=7)),
    Column('EAN', VARCHAR(length=13)),
    Column('titleImdb', VARCHAR(length=64)),
    Column('titleOrig', VARCHAR(length=64)),
    Column('titleLocal', VARCHAR(length=64)),
    Column('medium', VARCHAR(length=8)),
    Column('diskNr', VARCHAR(length=8)),
    Column('directed_by', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].create()
    pre_meta.tables['movie'].columns['directed_by'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].drop()
    pre_meta.tables['movie'].columns['directed_by'].create()
