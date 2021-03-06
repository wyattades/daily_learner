from abc import ABCMeta, abstractmethod
import pickle
import numpy as np
from keras.models import Model

class MLmodel(object):

    __metaclass__ = ABCMeta
    
    __model = None

    def __init__(self):
        pass

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

        :return: dict
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
    def load_model(self, model_bin):
        """

        :param model_bin:
        A binary (pickle) representation of the model
        :return:
        None
        """
        pass

    @abstractmethod
    def save_model(self):
        """
            saves model using pickel using a string representation
        :return:
            a json representation of the model
        """
        pass
        