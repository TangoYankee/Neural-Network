from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from models import db_connect, create_tables
from sql_manager import Pipeline

engine = db_connect()
create_tables(engine)
Session = sessionmaker(bind=engine)

data_file_name = "cancer_data.csv"
k_folds = 5
# "cancer_data.csv"
# "ep_data.csv"
# "pnn_data.csv"

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def main():
    with session_scope() as session:
    #     print("Clear Data")
    #     Pipeline().clear_data(session)
        # print("Load Data")
        # Pipeline().load_data(session, data_file_name)
        # Pipeline().print_all(session)
        # print("Assign folds")
        # Pipeline().assign_folds(session, k_folds)
        # Pipeline().print_all(session)
        # print("clear folds")
        # Pipeline().clear_folds(session)  
        Pipeline().print_all(session)   

if __name__ == "__main__":
    main()