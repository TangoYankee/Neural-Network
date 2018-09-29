"""
Define the SQL Data Session and control the flow of the Neural Network
"""
from contextlib import contextmanager
import os
import csv
import sys
sys.path.insert(0, './')
import settings
import models as mdls
from sqlalchemy.orm import sessionmaker

ENGINE = mdls.db_connect()
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

def get_from_csv(file_name):
    """Before the database is initialized, data are stored in csv files. 
       This function is called by def load_data"""
    data_open = open(os.path.join(settings.DATA_DIR, file_name))
    return csv.DictReader(data_open)

def check_database(file_name):
    if file_name == settings.CANCER_DATA:
        database = mdls.CancerData
    elif file_name == settings.EP_DATA:
        database = mdls.EpData
    elif file_name == settings.PNN_DATA:
        database = mdls.PnnData
    else:
        sys.exit('data file does not match existing database')
    return database

##TODO: 
# 1. Function to make values floats and true values integers
# 2. Function to add row of data to sql database  
#   - Will need way to generalize models in add functions
# 3. Standardized way to track and check file names, avoiding hard-coding of file names outside of settings 
# 4. Standardized way to track names of tables and link to file names

def load_data():
    """  Control the flow of the Neural Network """
    with session_scope() as session:
        file_name = settings.DATA_FILE_NAMES[0]
        database = check_database(file_name)
        dataDict = get_from_csv(file_name)
        for data in dataDict:
            float_value = float(data["val_one"])
            print (type(float_value))
            print (float_value)
        
load_data()
