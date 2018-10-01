"""
Define the SQL Data Session and control the flow of the Neural Network
"""
import models as mdls

# K_FOLDS = 5

def main():
    """  Control the flow of the Neural Network """
    with mdls.session_scope() as session:
        print("Cancer")
        for each_item in session.query(mdls.CancerData).all():
            print(each_item.id, each_item.var_one, each_item.fold)
        print("EP")
        for each_item in session.query(mdls.EpData).all():
            print(each_item.id, each_item.var_one, each_item.fold)
        print("PNN")
        for each_item in session.query(mdls.PnnData).all():
            print(each_item.id, each_item.var_one, each_item.fold)
        
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
