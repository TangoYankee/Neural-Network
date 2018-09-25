"""
Manipulation of the sql database, including adding data from csv file, clearing data from the database, and changing the assignment of folds. 
"""

import os
import random
import csv

from models import RawData
import settings


def get_from_csv(file_name):
    """Before the database is initialized, data are stored in csv files. 
       This function is called by def load_data"""
    data_open = open(os.path.join(settings.DATA_DIR, file_name))
    return csv.reader(data_open)


def format_data_row(data_row):
    """
    Structure of CSV columns do not initially meet structure of SQL Database
    This function is used by def load_data.
    """
    return {'values': list(map(float, data_row))}

def generate_folds_list(data, k_folds):
    """
    K-Fold cross validation depends on randomly assigning all values to 'k' variables of folds
    Data will not always divide evenly into k folds. Remainders must be evenly distributed after 
    initial distribution. It relies on sampling without replacement; this may create an error if the 
    number of remainders is greater than the standard fold size.
    This function is used by def load_data.
    """
    data_length = len(data)
    fold_size = data_length // k_folds
    remainders = data_length % k_folds

    folds_list = []
    for x in range(k_folds):
        folds_list += [x+1]*fold_size
    # TODO: Change to 'with replacement' sampling. Hint: random.choices not currently working 
    folds_list += random.sample(folds_list, remainders)
    random.shuffle(folds_list)
    return folds_list

class Pipeline(object):
    def add_item(self, session, data):
        """
        Each row is added to the session individually
        """
        session.add(RawData(**data))

    def load_data(self, session, file_name):
        """
        Data is initially stored in csv and must be moved into database
        """
        for each_training_row in get_from_csv(file_name):
            self.add_item(session, format_data_row(each_training_row))

    def clear_data(self, session):
        """
        Reset the table to start over with all fresh data
        """
        session.query(RawData).delete()

    def assign_folds(self, session, k_folds):
        """
        Data must be randomly distributed into training and testing folds. 
        These assignments stay the same through a training session. 
        """
        data = session.query(RawData).all()
        folds_list = generate_folds_list(data, k_folds)
        x = 0
        for each_data in data:
            each_data.fold = folds_list[x]
            x += 1

    def clear_folds(self, session):
        """
        Cross-Validation fold assignments can be changed for a new training session. However, current assignments
        must be reset first. 
        """
        for each_item in session.query(RawData).all():
            each_item.fold = 0
    
    def print_all(self, session):
        """
        Allows for visually inspection data and k-fold quality
        """
        for each_item in session.query(RawData).all():
            print(each_item.id, each_item.values, each_item.fold)
    