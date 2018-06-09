from sqlalchemy.orm import sessionmaker
from models import Tests, db_connect, create_test_table
from sqlalchemy.engine.url import URL

import numpy
import math
import csv
import random
import settings

class LivingSocialPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_test_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item):
        session = self.Session()
        test = Tests(**item)

        try:
            session.add(test)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
    
    # def display_item(ident):
    #     session = self.Session()
    #     session.query(Tests).filter(Tests.id == ident)