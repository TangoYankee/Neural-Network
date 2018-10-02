"""
Define the SQL Data Session and control the flow of the Neural Network
"""
import math
import numpy
from pick import pick
import models
import manage_folds
import feed_forward

def sigmoid(x):
    return 1/(1+math.exp(-x))

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
        # fold_manager = manage_folds.FoldManager(database, session)
        # fold_manager.assign_folds() #Folds are assigned at the beginning of training
        # fold_manager.print_folds()

        #TODO: Feed Forward!!
        ## Only select data in the training folds
        feed_forwarder = feed_forward.FeedForward(database, session)
        hidden_matrix = feed_forwarder.build_hidden_matrix
        cancer_matrix = feed_forwarder.cancer_matrix_factory
        output_array = []
        for cancer_array in cancer_matrix:
            output_matrix = []
            for hidden_array in hidden_matrix:
                array_product = cancer_array*hidden_array
                output_matrix.append(sum(array_product))
            output_matrix_wieghts = numpy.random.rand(1, 3)
            output = output_matrix*output_matrix_wieghts
            sum_output = sum(output[0])
            output_array.append(sigmoid(sum_output))
        print("output array: ", output_array)
        ##TODO: Back Propagate


        # fold_manager.clear_folds() #Folds are reset at the end of training
        # fold_manager.print_folds()

if __name__ == "__main__":
    main()
