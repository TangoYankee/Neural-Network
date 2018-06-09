from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_test_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Tests(DeclarativeBase):
    __tablename__ = 'test'

    id = Column(Integer, primary_key = True)
    title = Column('title', String)
    link = Column('link', String, nullable=True)
    location = Column('location', String, nullable=True)
    original_price = Column('original_price', Integer, nullable=True)
    price = Column('price', Integer, nullable=True)
    end_date = Column('end_date', DateTime, nullable = True)