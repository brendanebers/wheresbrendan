from sqlalchemy.dialects.postgresql import *
from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
position = Table('position', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('epoch', Integer),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('country', Unicode),
    Column('city', Unicode),
    Column('distance_from_prev', Float),
    Column('time_from_prev', Float),
    Column('speed_from_prev', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['position'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['position'].drop()
