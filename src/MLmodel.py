from abc import ABCMeta, abstractmethod


class MLmodel(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def upload_data(self, data_frame):
        """
        data_frame = A list of lists of floats corresponding to input data

            Loads the data and divides it in to training and testing sets
            Preps data for training.

        :return:
        None
        """
        pass

    @abstractmethod
    def train(self):
        """
            Trains the model and stores it in the regr class feild

        :return:
        List<float>: A list of all of the coefficents found
        float: Mean Squared Error
        float: R score
        """
        pass

    @abstractmethod
    def predict(self, data_in):
        """
        Predicts based on training
        :param data_in:
        a list of input values for the model to predict based upon
        :return:
        float = the prediciton result
        """
        pass

    @abstractmethod
    def load_model(self, model_string):
        """

        :param model_string:
        A string representation of the model found using pickel
        :return:
        None
        """

    @abstractmethod
    def save_model(self):
        """
            saves model using pickel using a string representation
        :return:
            a string representation of the model
        """