"""
Define the SQL Data Session and control the flow of the Neural Network
"""
import models as mdls

K_FOLDS = 5

def main():
    """  Control the flow of the Neural Network """
    with mdls.session_scope() as session:
        print("hello, session")
        # print("Clear Data")
        # Pipeline().clear_data(session)
        # print("Load Data")
        # Pipeline().load_data(session, DATA_FILE_NAME)        # Pipeline().print_all(session)
        # print("Assign folds")
        # Pipeline().assign_folds(session, K_FOLDS)
        # Pipeline().print_all(session)
        # print("clear folds")
        # Pipeline().clear_folds(session)
        # Pipeline().print_all(session)

if __name__ == "__main__":
    main()
