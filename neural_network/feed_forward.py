"""
Calculate Output of current settings for Neural Network
"""
import sys
sys.path.insert(0, './')
import settings
import numpy

class FeedForward():
    """
    Object to share variables and functions common to database
    """
    def __init__(self, database, session):
        self.database = database
        self.session = session
        self.query_all_data
        self.calc_variable_count

    @property
    def calc_variable_count(self):
        """
        Wieght Matrix is determined by number of variables in database
        Determine the number of variables in a given row of data
        Length determination will change once database changes. For now, subtract length by 4 (id, true_value, fold, misc value)
        """
        single_result = self.session.query(self.database).first()
        row_length = len(single_result.__dict__)
        self.variable_count = row_length - settings.SQL_COLUMNS
        return self.variable_count

    @property
    def query_all_data(self):
        """
        Make all data a property, to allow all functions to act on data without 
        generating new query
        """
        self.all_data = self.session.query(self.database).all()
        return self.all_data

    @property
    def build_hidden_matrix(self):
        self.hidden_matrix = numpy.random.rand(settings.HIDDEN_LAYER_NODES, self.variable_count)
        return self.hidden_matrix

    @property
    def cancer_matrix_factory(self):
        var_matrix = []
        for data in self.all_data:
            var_matrix.append([data.var_one, data.var_two, data.var_three, 
            data.var_four, data.var_five, data.var_six, data.var_seven,
            data.var_eight, data.var_nine])
        return var_matrix


## Factory to handle the variables of each 

## Create a matrix that has three hidden layers multiplied by the number of variables in the row of data
## Create a database to hold the matrix. 
#   Each neural network will need its own database, as the dimensions are unique
#   Its width (number of columns) should be the number of variables in the row of input data. 
#   Its length (number of rows) should be equal to number of nodes in the hidden layer
#   Each row should contain the result of inputting all the data from the previous layer
#     A column of calculated value
#     Calculate Value is reset between each input of data value
#     Values of matrix remains the same until the back-propogation step
## The value of each hidden layer node is calculated by 
#    mulitplying the weights of link between an input layer and hidden layer nodes.
#    Adding together the product of each weight multiplied by input value
## Calculated value is reset after recording final output value
## Repeat matrix generation, database collection, calculated value collection with output layer
#    Matrix will have three columns (inputs are from three hidden layer nodes)
#    Matrix will have number of rows equal to number of data sets. Because only one row is required per dataset, it can store the predicted value
## Future iterations: Biases and Activation Functions