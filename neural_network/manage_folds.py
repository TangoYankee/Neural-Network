"""
Manipulation of the sql database to randomly assign and then reset data values to and from the sql database
"""
import random
import sys
sys.path.insert(0, './')
import settings


class FoldManager:
    """
    Database and SQL Session are shared by all of the associated functions. 
    """
    def __init__(self, database, session):
        self.database = database
        self.session = session
        self.all_data = session.query(database).all()

    def user_set_folds(self):
        """
        Number of folds is withheld from the global realm until it can be assured that its 
        characteristics of a user defined function can be preserved.
        """
        k_default = settings.K_FOLDS_DEFAULT
        k_top = settings.K_FOLDS_TOP_LIMIT
        k_bottom = settings.K_FOLDS_BOTTOM_LIMIT

        exit_loop = 5
        counter = 0
        k_folds = None
        while (not k_folds) & (counter<exit_loop):
            try:
                k_input = int(input("Select number of folds, between {0} and {1}: ".format(k_bottom, k_top)))
                if (k_bottom <= k_input <= k_top):
                    k_folds = k_input
                else:
                    print("The inputted value was not between {0} and {1}.".format(k_bottom, k_top))
                    counter+=1
            except ValueError:
                counter+=1
                print("The inputted value was not an integer")
        # Set to default value if user fails to choose an option
        if not k_folds:
            print("Failed to input a valid option. Setting Number of Folds to {0}".format(k_default))
            k_folds = k_default    
        print("number of folds: {0}".format(k_folds))
        return k_folds

    def generate_folds_list(self, k_folds):
        """
        K-Fold cross validation depends on randomly assigning all values to 'k' variables of folds
        Data will not always divide evenly into k folds. Remainders must be evenly distributed after 
        initial distribution. It relies on sampling without replacement; this may create an error if the 
        number of remainders is greater than the standard fold size.
        This function is used by def load_data.
        """
        data_length = len(self.all_data)
        fold_size = data_length // k_folds
        remainders = data_length % k_folds

        folds_list = []
        for fold_assignment in range(k_folds):
            folds_list += [fold_assignment]*fold_size
        # TODO: Change to 'with replacement' sampling. Hint: random.choices not currently working 
        folds_list += random.sample(folds_list, remainders)
        random.shuffle(folds_list)
        return folds_list

    def assign_folds(self):
        """
        Data must be randomly distributed into training and testing folds. 
        These assignments stay the same through a training session. 
        """
        k_folds = self.user_set_folds()
        folds_list = self.generate_folds_list(k_folds)
        list_position = 0
        for each_data in self.all_data:
            each_data.fold = folds_list[list_position]
            list_position+=1

    def clear_folds(self):
        """
        Cross-Validation fold assignments can be changed for a new training session. However, current assignments
        must be reset first. 
        """
        for each_item in self.all_data:
            each_item.fold = None

    def print_folds(self):
        """
        Allows for visually inspection data and k-fold quality
        """
        for each_item in self.all_data:
            print("Item ID: {0}, Fold Number: {1}".format(each_item.id, each_item.fold))
    