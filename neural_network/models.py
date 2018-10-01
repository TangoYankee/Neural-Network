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
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

ENGINE = sa.create_engine(URL(**settings.DATABASE))
SESSION = sessionmaker(bind=ENGINE)

@contextmanager
def session_scope():
    """ Control the SQL Database Session  """
    session = SESSION()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

class Base(object):
    """Characteristics common to all tables"""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer, primary_key=True)
    true_value = sa.Column(sa.Integer)
    fold = sa.Column(sa.Integer, default=None)

    #TODO: Function to print and check values of database
    # TODO: Function to assign Folds
    #TODO: Function to clear Fold Assignment
    

Base = declarative_base(cls=Base)

##TODO: Add variables to hold weights of variables linked to hidden layer
# TODO: Add class for hidden layer network
# TODO: Add class for output layer network
# TODO: Add place to biases and activation functions

class CancerData(Base):
    """
    Names of Variables are unknown
    """
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
    """
    Names of Variables are unknown
    """
    var_one = sa.Column(sa.Float)
    var_two = sa.Column(sa.Float)
    var_three = sa.Column(sa.Float)
    var_four = sa.Column(sa.Float)
    var_five = sa.Column(sa.Float)
    var_six = sa.Column(sa.Float)

class PnnData(Base):
    """
    Names of Variables are unknown
    """
    var_one = sa.Column(sa.Float)
    var_two = sa.Column(sa.Float)
    var_three = sa.Column(sa.Float)
    