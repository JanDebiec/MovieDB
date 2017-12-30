from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
movie = Table('movie', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('imdbId', String(length=7)),
    Column('EAN', String(length=13)),
    Column('titleImdb', String(length=64)),
    Column('titleOrig', String(length=64)),
    Column('titleLocal', String(length=64)),
    Column('medium', String(length=8)),
    Column('diskNr', String(length=8)),
    Column('directed_by', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['movie'].columns['directed_by'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['movie'].columns['directed_by'].drop()
