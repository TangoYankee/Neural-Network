"""
SQLAlchemy database structuring
"""

from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.engine.url import URL

import settings

def db_connect():
    """Initialize Database Connection"""
    return create_engine(URL(**settings.DATABASE))

def create_tables(ENGINE):
    """Format Data Structure"""
    Base.metadata.create_all(ENGINE)

class Base(object):
    """Characteristics common to all tables"""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    values = Column(postgresql.ARRAY(Float))

Base = declarative_base(cls=Base)

class RawData(Base):
    """Value to hold fold of K-Fold cross-validation"""
    fold = Column(Integer, default = 0)
    