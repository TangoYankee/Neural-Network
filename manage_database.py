# from sqlalchemy.orm import sessionmaker
from models import TrainingData
# , db_connect, create_tables
# from sqlalchemy.engine.url import URL
# from sqlalchemy.engine import reflection

# import numpy
# import math
# import csv
# import random
# import settings

# class BasePipeline(object):
#     def __init__(self):
#         self.engine = db_connect()
#         create_tables(self.engine)
#         self.Session = sessionmaker(bind=self.engine)

#     def process_cancer(self, data):
#         cancer = CancerData(**data)
#         self.add_item(cancer)

#     def process_ep(self, data):
#         ep = EPData(**data)
#         self.add_item(ep)

#     def process_pnn(self, data):
#         pnn = PNNData(**data)
#         self.add_item(pnn)
    
#     def add_item(self, data):
#         session = self.Session()
#         try:
#             session.add(data)
#             session.commit()
#             print("success")
#         except:
#             session.rollback()
#             print("failure")
#             raise
#         finally:
#             session.close()
#         return data
    
#     def query_database(self):
#         session = self.Session()
#         try:
#             for row in session.query(CancerData).all():
#                 print(row.id, row.values)
#         except:
#             session.rollback()
#             print("failure")
#             raise
#         finally:
#             session.close()

#     def reset(self):
#         session = self.Session()
#         session.query(CancerData).delete()
#         session.commit()

class Pipeline(object):
    def add_item(self, session, data):
        training_data = TrainingData(**data)
        session.add(training_data)

    def reset(self, session):
        session.query(TrainingData).delete()

    def print_all(self, session):
        for row in session.query(TrainingData).all():
            print(row.id, row.values, row.fold)