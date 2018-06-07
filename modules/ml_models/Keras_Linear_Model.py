from MLmodel import MLmodel
from Exceptions import ToSmallDataSetException
from Exceptions import IncorrectPredictSizeException

import pickle
from keras.models import Sequential, Model
from keras.layers import Dense
from keras import backend, optimizers
from sklearn.metrics import mean_squared_error,  r2_score
import numpy as np
np.random.seed(7)

from time import sleep

class LinearModel(MLmodel):

    __data = []
    __train_data = []
    __test_data = []
    __results = []
    __train_results = []
    __test_results = []
    __num_attributes = 0
    __num_entries = 0
    __model = None

    def train(self):
        self.__model = Sequential()
        self.__model.add(Dense(20, activation="linear", input_dim=self.__num_attributes, kernel_initializer="normal"))
        self.__model.add(Dense(20, activation="linear", kernel_initializer="normal"))
        self.__model.add(Dense(1, activation="linear", kernel_initializer="normal"))
        self.__model.compile(loss='mse', optimizer='adam')
        self.__model.fit(self.__train_data, self.__train_results, epochs=500, batch_size=1000, validation_split=0.3, verbose=0)
        res = self.__model.predict(self.__test_data)
        return dict(error=mean_squared_error(res,self.__test_results), score=r2_score(res, self.__test_results))

    def predict(self, data_in):
        res = self.__model.predict(np.asarray(data_in).reshape(1,-1))
        print('--- predicted', res)
        return float(res[0])


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

    def load_model(self, model_bin):
        model_data = pickle.loads(model_bin)
        m_model, m_weights = model_data['model'], model_data['weights']

        self.__model = Sequential.from_config(m_model)
        self.__model.set_weights(np.array(m_weights))

    def save_model(self):
        m_model = self.__model.get_config()
        m_weights = self.__model.get_weights()
        return pickle.dumps(dict(model=m_model, weights=m_weights))
