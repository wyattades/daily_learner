from MLmodel import MLmodel
from Exceptions import ToSmallDataSetException
from Exceptions import IncorrectPredictSizeException

from sklearn import preprocessing
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential, Model
from keras.layers import Dense
from keras import backend, optimizers
import json
import numpy as np
from numpy import genfromtxt
np.random.seed(7)

class BlackBoxModel(MLmodel):

    __data = []
    __train_data = []
    __test_data = []
    __results = []
    __train_results = []
    __test_results = []
    __X_scale = None
    __Y_scale = None
    __X_scaled = []
    __Y_scaled = []
    __num_attributes = 0
    __num_entries = 0
    __model = None
    __name = ""

    def __init__(self, name):
        self.__name = name

    def train(self):
        model = Sequential()
        model.add(Dense(8, input_dim=self.__num_attributes, kernel_initializer='normal', activation='relu'))
        model.add(Dense(20, kernel_initializer='normal', activation='sigmoid'))
        model.add(Dense(1, kernel_initializer='normal'))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(self.__X_scaled, self.__Y_scaled, epochs=10, batch_size=1000, validation_split=0.3, verbose=1)
        self.__model = model
        res = self.__predict_arr(self.__test_data)
        return dict(error=mean_squared_error(res,self.__test_results), score=r2_score(res, self.__test_results))


    def predict(self, data_in):
        data_in = self.__X_scale.transform(np.float32(data_in).reshape(1,-1))
        return self.__Y_scale.inverse_transform(self.__model.predict(data_in))

    def __predict_arr(self, data_in):
        data_in = self.__X_scale.transform(np.float32(data_in))
        return self.__Y_scale.inverse_transform(self.__model.predict(data_in))


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
        self.__X_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
        self.__Y_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
        self.__X_scaled = self.__X_scale.fit_transform(self.__train_data)
        self.__Y_scaled = self.__Y_scale.fit_transform(self.__train_results)

    def load_model(self, model_json):
        model_data = json.loads(model_json)
        self.__model = Model.from_config(model_data.model)
        self.__model.set_weights(np.array(model_data.weights))
        # with open(self.__name+'blackbox.h5', 'w') as myfile:
        #     myfile.write(weights)
        # self.__model.load_weights(self.__name + 'blackbox.h5')

    def save_model(self):
        m_model = self.__model.get_config()
        m_weights = self.__model.get_weights()
        return json.dumps(dict(model=m_model, weights=m_weights))
        # m_weights = self.__model.save_weights(self.__name+"blackbox.h5")
        # with open(self.__name+'blackbox.h5', 'r') as myfile:
        #     m_weights= myfile.read()
        # return m_weights, m_json


# def upload_data_test():
#     s = BlackBoxModel("Test")
#     DB_LOC = "/mnt/FireCuda/Documents/School/Spring_2018/CMPS183/Keras_test/venv/prices.csv"
#     my_data = genfromtxt(DB_LOC, delimiter=',')[1:,:]
#     s.upload_data(my_data)
#     s.train()
#     weights,json = s.save_model()
#     s = BlackBoxModel("Test")
#     s.upload_data(my_data)
#     s.load_model(json,weights)
#     res = s.predict([10,11,10])
#     print(res)

# upload_data_test()



