"""
Define the SQL Data Session and control the flow of the Neural Network
"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from models import db_connect, create_tables
from sql_manager import Pipeline

ENGINE = db_connect()
create_tables(ENGINE)
SESSION = sessionmaker(bind=ENGINE)

DATA_FILE_NAME = "cancer_data.csv"
K_FOLDS = 5
# "cancer_data.csv"
# "ep_data.csv"
# "pnn_data.csv"

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

def main():
    """  Control the flow of the Neural Network """
    with session_scope() as session:
    #     print("Clear Data")
    #     Pipeline().clear_data(session)
        # print("Load Data")
        # Pipeline().load_data(session, DATA_FILE_NAME)        # Pipeline().print_all(session)
        # print("Assign folds")
        # Pipeline().assign_folds(session, K_FOLDS)
        # Pipeline().print_all(session)
        # print("clear folds")
        # Pipeline().clear_folds(session)
        Pipeline().print_all(session)

if __name__ == "__main__":
    """ Run the Neural Network  """
    main()
