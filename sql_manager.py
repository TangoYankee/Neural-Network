import os
import random
import csv

from models import TrainingData
import settings

def get_from_csv(file_name):
    data_open = open(os.path.join(settings.DATA_DIR, file_name))
    return csv.reader(data_open)

def format_data_row(data_row):
    return {'values': list(map(float, data_row))}

class Pipeline(object):
    def add_item(self, session, data):
        session.add(TrainingData(**data))

    #Pull data from a csv and load it into sql
    def load_data(self, session, file_name):
        for each_training_row in get_from_csv(file_name):
            self.add_item(session, format_data_row(each_training_row))

    def clear_data(self, session):
        session.query(TrainingData).delete()

    def get_all_id(self, session):
        return session.query(TrainingData.id).all()
    
    #Withhold one-fifth of the data for training validation
    #Function achieves this by randomly selecting a list of rows
    #that will have their fold value changed from True to False
    def withhold_fold(self, session, fold_divider):
        id_data = self.get_all_id(session)
        withhold_list = random.sample(id_data, len(id_data)//fold_divider)
        for each_withhold in withhold_list:
            datum = session.query(TrainingData).get(each_withhold.id)
            datum.fold = False

    #Set all data to be in training set
    def clear_withhold(self, session):
        for each_item in session.query(TrainingData).all():
            each_item.fold = True
    
    def print_all(self, session):
        for each_item in session.query(TrainingData).all():
            print(each_item.id, each_item.values, each_item.fold)
    