"""
Define the SQL Data Session and control the flow of the Neural Network
"""
from pick import pick
import models
import manage_folds


def user_select_database():
    """
    User can choose 
    """
    title = "Choose a database to train the neural network"
    options = [models.CancerData, models.EpData, models.PnnData]
    database, index = pick(options, title)
    print("Selected Database: {0}, (choice #{1})".format(database, index))
    return database  
    
def main():
    """  Control the flow of the Neural Network """
    database = user_select_database()
    with models.session_scope() as session:
        fold_manager = manage_folds.FoldManager(database, session)
        fold_manager.assign_folds() #Folds are assigned at the beginning of training
        # fold_manager.print_folds()
        #TODO: Train the Network!!
        fold_manager.clear_folds() #Folds are reset at the end of training
        # fold_manager.print_folds()

if __name__ == "__main__":
    main()
