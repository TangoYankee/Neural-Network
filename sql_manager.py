import os
import random
import csv

from models import RawData, TestData
import settings

#Used by def load_data
def get_from_csv(file_name):
    data_open = open(os.path.join(settings.DATA_DIR, file_name))
    return csv.reader(data_open)

#Used by def load_data
def format_data_row(data_row):
    return {'values': list(map(float, data_row[:-1])), 'true_value': data_row[-1]}

#Used by def assign folds
# Generate a list of equal length to data set
# Create k groups of integers of equal size
# Randomly distribute remainders to different folds
def generate_folds_list(data, k_folds):
    data_length = len(data)
    fold_size = data_length // k_folds
    remainders = data_length % k_folds

    folds_list = []
    for x in range(k_folds):
        folds_list += [x]*fold_size
    #Sampling without replacement. May create error if remainders greater than standard fold size
    # TODO: Change to with replacement. Hint: random.choices not working 
    folds_list += random.sample(folds_list, remainders)
    random.shuffle(folds_list)
    return folds_list

class Pipeline(object):
    def add_item(self, session, data):
        session.add(RawData(**data))

    #Pull data from a csv and load it into sql
    def load_data(self, session, file_name):
        for each_training_row in get_from_csv(file_name):
            self.add_item(session, format_data_row(each_training_row))

    #Remove all of the data from the Model's table
    def clear_data(self, session):
        session.query(RawData).delete()

    #K-Fold Cross Validation
    def assign_folds(self, session, k_folds):
        data = session.query(RawData).all()
        folds_list = generate_folds_list(data, k_folds)
        x = 0
        for each_data in data:
            each_data.fold = folds_list[x]
            x += 1

    #Reset all fold assignments to default
    def clear_folds(self, session):
        for each_item in session.query(RawData).all():
            each_item.fold = None
    
    def print_all(self, session):
        for each_item in session.query(RawData).all():
            print(each_item.id, each_item.values, each_item.fold)
    
    def get_training_folds(self, session, fold_value):
        return session.query(RawData).filter(RawData.fold != fold_value).all()

class TestDataManager(object):
    #Pull data from a csv and load it into sql
    def load_data(self, session, file_name):
        for each_training_row in get_from_csv(file_name):
            # print (format_data_row(each_training_row))
            self.add_item(session, format_data_row(each_training_row))

    def add_item(self, session, data):
        session.add(TestData(**data))

    #Remove all of the data from the Model's table
    def clear_data(self, session):
        session.query(TestData).delete()

    def print_all(self, session):
        for each_item in session.query(TestData).all():
            print(each_item.values, each_item.id, each_item.true_value, each_item.fold)

    #K-Fold Cross Validation
    def assign_folds(self, session, k_folds):
        data = session.query(TestData).all()
        folds_list = generate_folds_list(data, k_folds)
        x = 0
        for each_data in data:
            each_data.fold = folds_list[x]
            x += 1

    #Reset all fold assignments to default
    def clear_folds(self, session):
        for each_item in session.query(TestData).all():
            each_item.fold = None
    
    def get_training_folds(self, session, fold_value):
        return session.query(TestData).filter(TestData.fold != fold_value).limit(5).all()