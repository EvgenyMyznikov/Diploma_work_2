from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = create_engine('postgres://...@localhost:5432/vkinder', echo=True)
metadata = MetaData()
candidates = Table('candidates', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('first_name', String),
                   Column('last_name', String),
                   Column('age_id', Integer))

candidates.create(bind=engine)

candidates_info = Table('candidates_info', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', Integer),
                        Column('city', String),
                        Column('sex', Integer),
                        Column('url', String, nullable=False))

candidates_info.create(bind=engine)
