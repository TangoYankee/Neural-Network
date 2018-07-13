from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
# from random import uniform
# from numpy import numpy.exp, dot
import numpy

from models import db_connect, create_tables
from sql_manager import Pipeline, TestDataManager

engine = db_connect()
create_tables(engine)
Session = sessionmaker(bind=engine)

data_file_name = "cancer_data.csv"
k_folds = 5
hidden_layer_size = 3
output_layer_size = 1
input_layer_size = 2
L = .1
epochs = 20000
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

def create_weight_arrays(first_layer_size, second_layer_size):
    return numpy.random.uniform(size=(first_layer_size, second_layer_size))    

def get_dot_product_array(weight_array, inputs):
    dot_product_array = []
    for input_set in inputs:
        dp = numpy.dot(weight_array, input_set.values)
        dot_product_array.append(dp)
    return dot_product_array    

#Activation and Derivative of Activation function
def sigmoid(x): return 1/(1 + numpy.exp(-x))
def sigmoid_(x): return x*(1-x)


def main():
    with session_scope() as session:
        # print("load data")
        # TestDataManager().load_data(session, data_file_name)
        # TestDataManager().print_all(session)
        # print("Clear Data")
        # TestDataManager().clear_data(session)
        # print("Load Data")
        # Pipeline().load_data(session, data_file_name)
        # TestDataManager().print_all(session)
        # print("Assign folds")
        # TestDataManager().assign_folds(session, k_folds)
        # TestDataManager().print_all(session)
        # print("clear folds")
        # Pipeline().clear_folds(session)  
        # Pipeline().print_all(session)
        # print (weight_array)
        training_folds = TestDataManager().get_training_folds(session, 0)
        
        values_array = []
        true_value_array = []
        for each_item in training_folds:
            values_array.append(each_item.values)
            true_value_array.append([each_item.true_value])
        X_test = numpy.array(values_array)
        # print(type(X_test))
        # X = numpy.array(values_array)
        # print(X)
        # Y = numpy.array(true_value_array)    
        # print(Y)
        # input_layer_size = len(values_array[0])
        # Wh = create_weight_arrays(input_layer_size, hidden_layer_size)
        # Wz = create_weight_arrays(hidden_layer_size, output_layer_size)
        

        X = numpy.array([[0,0], [0,1], [1,0], [1,1]])
        # print(type(X))
        Y = numpy.array([ [0],   [1],   [1],   [0]])
                                                         # weights on layer inputs
        Wh = numpy.random.uniform(size=(input_layer_size, hidden_layer_size))
        Wz = numpy.random.uniform(size=(hidden_layer_size, output_layer_size))
        
        # for i in range(epochs):
        
        #     H = sigmoid(numpy.dot(X, Wh))                  # hidden layer results
        #     Z = numpy.dot(H,Wz)                            # output layer, no activation
        #     E = Y - Z                                   # how much we missed (error)
        #     dZ = E * L                                  # delta Z
        #     Wz +=  H.T.dot(dZ)                          # update output layer weights
        #     dH = dZ.dot(Wz.T) * sigmoid_(H)             # delta H
        #     Wh +=  X.T.dot(dH)                          # update hidden layer weights
            
        # print(Z)               # what have we learnt?
# test_values = numpy.array(values_array)
        # test_true_value = numpy.array(true_value_array)    
        # input_layer_size = len(values_array[0])
        # hidden_weights = create_weight_arrays(input_layer_size, hidden_layer_size)
        # output_weights = create_weight_arrays(hidden_layer_size, output_layer_size)
        
        #Start ANN
        # hidden_layer_results = sigmoid(numpy.dot(test_values, hidden_weights))
        # output_layer_results = sigmoid(numpy.dot(hidden_layer_results, output_weights))
        # error = test_true_value - output_layer_results
        # delta_output_layer = error * sigmoid_(output_layer_results)
        # delta_hidden_layer = delta_output_layer.dot(output_weights.T) * sigmoid_(hidden_layer_results)
        # output_weights += hidden_layer_results.T.dot(delta_output_layer)
        # hidden_weights += test_values.T.dot(delta_hidden_layer)

        # print(output_layer_results)
        # print(len(output_layer_results))

if __name__ == "__main__":
    main()