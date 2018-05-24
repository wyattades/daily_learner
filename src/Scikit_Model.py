from MLmodel import MLmodel
from Exceptions import ToSmallDataSetException
from Exceptions import IncorrectPredictSizeException
import numpy as np
from numpy import genfromtxt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pickle


class ScikitModel(MLmodel):



    __data = []
    __train_data = []
    __test_data = []
    __results = []
    __train_results = []
    __test_results = []
    __num_attributes = 0
    __num_entries = 0
    __regr = None
    __name = ""

    def __init__(self, name):
        self.__name = name

    def train(self):
        self.__regr = linear_model.LinearRegression()
        self.__regr.fit(self.__train_data, self.__train_results)
        test_pred = self.__regr.predict(self.__test_data)
        return [self.__regr.coef_, mean_squared_error(self.__test_results, test_pred),
                r2_score(self.__test_results, test_pred)]

    def predict(self, data_in):
        if(len(data_in) != self.__num_attributes):
            raise IncorrectPredictSizeException("Error predicting, input size does not match model")
        res = self.__regr.predict(np.asarray(data_in).reshape(1,-1))
        return res[0]

    def upload_data(self, data_frame):
        if(len(data_frame) < 5):
            raise ToSmallDataSetException("Data set is to small for reasonable results")
        self.__num_attributes = len(data_frame[0]) - 1
        self.__num_entries = len(data_frame)
        self.__data = np.zeros((self.__num_entries,self.__num_attributes))
        self.__results = np.zeros((self.__num_entries,1))

        row_counter = 0
        for i in data_frame:
            self.__data[row_counter,:] = i[0:-1]
            self.__results[row_counter,0] = i[-1]
            row_counter += 1

        train_test_split = (int)(self.__num_entries/4.0)
        self.__train_data = self.__data[train_test_split:,:]
        self.__test_data = self.__data[:train_test_split,:]
        self.__train_results = self.__results[train_test_split:,:]
        self.__test_results = self.__results[:train_test_split,:]

    def load_model(self, pk_file_in):
        with open(pk_file_in, 'rb') as file:
            self.__regr = pickle.load(file)

    def save_model(self):
        pk_filename = self.__name + ".pk1"
        with open(pk_filename, 'wb') as file:
            pickle.dump(self.__regr, file)
        return pk_filename


def upload_data_test():
    s = ScikitModel("Test")
    DB_LOC = "/home/leo/Documents/School/Spring2018/CMPS183/project/src/DataSets/AMarch.csv"
    my_data = genfromtxt(DB_LOC, delimiter=',')[1:,:]
    s.upload_data(my_data)
    s.train()
    pk_Model = s.save_model()
    s = ScikitModel("Test")
    s.upload_data(my_data)
    s.load_model(pk_Model)
    res = s.predict([8000,9500,9000])
    print res
upload_data_test()




