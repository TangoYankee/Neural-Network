from sqlalchemy import create_engine, Column, Float, Integer, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.engine.url import URL

import settings

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_tables(engine):
    Base.metadata.create_all(engine)

class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    values = Column(postgresql.ARRAY(Float))

Base = declarative_base(cls=Base)

class TrainingData(Base):
    fold = Column(Boolean, default=True)
    