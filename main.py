from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from models import db_connect, create_tables
from hello_world import Pipeline

engine = db_connect()
create_tables(engine)
Session = sessionmaker(bind=engine)

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
    data = {
        'fold': False,
        'values': [0.098, 0.872762, 0.12, 0.563]
    }
    with session_scope() as session:
        # Pipeline().add_item(session, data)
        Pipeline().print_all(session)
        Pipeline().reset(session)
        Pipeline().print_all(session)
        

if __name__ == "__main__":
    main()