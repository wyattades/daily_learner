from MLmodel import MLmodel
from Exceptions import ToSmallDataSetException
from Exceptions import IncorrectPredictSizeException

import numpy as np
from numpy import genfromtxt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


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
        return dict(error=mean_squared_error(self.__test_results, test_pred), score=r2_score(self.__test_results, test_pred))

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

    def load_model(self, model_json):
        pass

    def save_model(self):
        return None


# def upload_data_test():
#     s = ScikitModel("Test")
#     DB_LOC = "/mnt/FireCuda/Documents/School/Spring_2018/CMPS183/web2py/applications/project/src/DataSets/AMarch.csv"
#     my_data = genfromtxt(DB_LOC, delimiter=',')[1:,:]
#     s.upload_data(my_data)
#     mse, rs = s.train()
#     pk_Model = s.save_model()
#     s = ScikitModel("Test")
#     s.load_model(my_data,None)
#     res = s.predict([9000,9000,9000])
#     print(mse)
#     print(rs)
# upload_data_test()




