"""
Define the SQL Data Session and control the flow of the Neural Network
"""
import os
import csv
import sys
sys.path.insert(0, './')
import settings
import models as mdls


def get_from_csv(file_name):
    """
    Files have headers and can be extracted as a dictionary with keys listed in header
    """
    data_open = open(os.path.join(settings.DATA_DIR, file_name))
    return csv.DictReader(data_open)

def check_database(file_name):
    """
    Each of the three data sets has a distinct data structure with its own SQL Table
    """
    if file_name == settings.CANCER_DATA:
        database = mdls.CancerData
        factory = cancer_data_factory
    elif file_name == settings.EP_DATA:
        database = mdls.EpData
        factory = ep_data_factory
    elif file_name == settings.PNN_DATA:
        database = mdls.PnnData
        factory = pnn_data_factory
    else:
        sys.exit('data file does not match existing database')
    return (database, factory)

def cancer_data_factory(cancer_data):
    """
    Variable names and types from database need to be mapped to the SQL Table
    """
    return {
        'var_one' : float(cancer_data['val_one']),
        'var_two' : float(cancer_data['val_two']),
        'var_three' : float(cancer_data['val_three']),
        'var_four' : float(cancer_data['val_four']),
        'var_five' : float(cancer_data['val_five']),
        'var_six' : float(cancer_data['val_six']),
        'var_seven' : float(cancer_data['val_seven']),
        'var_eight' : float(cancer_data['val_eight']),
        'var_nine' : float(cancer_data['val_nine']),
        'true_value' : int(cancer_data['true_value']),   
    }

def ep_data_factory(ep_data):
    """
    Variable names and types from database need to be mapped to the SQL Table
    """
    return{
        'var_one' : float(ep_data['val_one']),
        'var_two' : float(ep_data['val_two']),
        'var_three' : float(ep_data['val_three']),
        'var_four' : float(ep_data['val_four']),
        'var_five' : float(ep_data['val_five']),
        'var_six' : float(ep_data['val_six']),
        'true_value' : int(ep_data['true_value'])   
    }

def pnn_data_factory(pnn_data):
    """
    Variable names and types from database need to be mapped to the SQL Table
    """
    return{
        'var_one' : float(pnn_data['val_one']),
        'var_two' : float(pnn_data['val_two']),
        'var_three' : float(pnn_data['val_three']),
        'true_value' : int(pnn_data['true_value'])   
    }

def add_data(database, factory_data, session):
    """
    All three data tables can use the same SQL add function
    """
    session.add(database(**factory_data))

def load_data():
    """
    Before the database is initialized, data are stored in csv files
    """
    with mdls.session_scope() as session:
        for file_name in settings.DATA_FILE_NAMES:
            database, factory = check_database(file_name)
            dataDict = get_from_csv(file_name)
            for data in dataDict:
                factory_data = factory(data)
                add_data(database, factory_data, session)
        
if __name__ == "__main__":
    load_data()

