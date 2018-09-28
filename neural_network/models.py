"""
SQLAlchemy database structuring
"""
import sys
sys.path.insert(0, './')
import settings

import sqlalchemy as sa 
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.engine.url import URL


def db_connect():
    """Initialize Database Connection"""
    return sa.create_engine(URL(**settings.DATABASE))

# def create_tables(ENGINE):
#     """Format Data Structure"""
#     Base.metadata.create_all(ENGINE)

class Base(object):
    """Characteristics common to all tables"""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer, primary_key=True)
    true_value = sa.Column(sa.Integer)
    fold = sa.Column(sa.Integer, default=None)

    #TODO: Function to assign Folds
    #TODO: Function to clear Fold Assignment

Base = declarative_base(cls=Base)

class CancerData(Base):
    """Value to hold fold of K-Fold cross-validation"""
    var_one = sa.Column(sa.Float)
    var_two = sa.Column(sa.Float)
    var_three = sa.Column(sa.Float)
    var_four = sa.Column(sa.Float)
    var_five = sa.Column(sa.Float)
    var_six = sa.Column(sa.Float)
    var_seven = sa.Column(sa.Float)
    var_eight = sa.Column(sa.Float)
    var_nine = sa.Column(sa.Float)    

class EpData(Base):
    var_one = sa.Column(sa.Float)
    var_two = sa.Column(sa.Float)
    var_three = sa.Column(sa.Float)
    var_four = sa.Column(sa.Float)
    var_five = sa.Column(sa.Float)
    var_six = sa.Column(sa.Float)

class PnnData(Base):
    var_one = sa.Column(sa.Float)
    var_two = sa.Column(sa.Float)
    var_three = sa.Column(sa.Float)
    