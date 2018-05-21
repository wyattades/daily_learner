import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import math
import sys

def read_csv(file_name):
    my_data = pd.read_csv(file_name, sep=',', header=0)
    df,enum_map = enum_data(my_data)
    return df.values,enum_map




def enum_column(labels,df):
    enum_map = dict()
    counter = 0
    for l in labels:
        df= df.replace(l, counter)
        enum_map[l] = counter
        counter += 1
    return df,enum_map


def enum_data(df):
    dict_list = []
    for i in df:
        enum_map = dict()
        if(isinstance(df[i][0],basestring)):
            label_list = []
            for j in range(0,len(df[i])):
                if(df[i][j]  not in label_list):
                    label_list.append(df[i][j])
            [df[i],enum_map] = enum_column(label_list,df[i])
        dict_list.append(enum_map)
        print(enum_map)
    return df,dict_list

def scikit_linear_train(df):
    [traindf, testdf] = np.array_split(df,2)
    regr = linear_model.LinearRegression()
    Xtrain = traindf[:,0:-1]
    Ytrain = traindf[:,-1]
    Xtest = testdf[:,0:-1]
    Ytest = testdf[:,-1]
    regr.fit(Xtrain, Ytrain)
    Ypred = regr.predict(Xtest)
    # The coefficients
    print('Coefficients: ' +  str(regr.coef_))
    # The mean squared error
    print("Mean squared error: " + str(mean_squared_error(Ytest, Ypred)))

    print('Variance score: ' + str(r2_score(Ytest, Ypred)))
    return regr


def scikit_perdict(regr, test,enum_map):
    for i in range(0,len(test)):
        if(enum_map[i] != {}):
            col_map = enum_map[i]
            test[i] = col_map[test[i]]
    enum_test = np.asarray(test).reshape(1,-1)
    print(enum_test)
    res = regr.predict(enum_test)
    if(enum_map[-1] == {}):
        print("Your result was: " + str(regr.predict(enum_test)))
    else:
        last_col = enum_map[-1]
        min_dist =  sys.maxint
        for i in last_col:
            dist = abs(last_col[i] - res)
            if(dist < min_dist):
                min_dist = dist
                result_string = i

        print("Your result was: " + result_string)

# Stock Market
#SAMPLE_DB = "/mnt/FireCuda/Documents/Personal/BackendML/venv/DataSets/AMarch.csv"

#Fruits
SAMPLE_DB = "/mnt/FireCuda/Documents/Personal/BackendML/venv/DataSets/fruits.csv"

df, enum_map = read_csv(SAMPLE_DB)
print(df)
regression_model = scikit_linear_train(df)

#StockMarket
#scikit_perdict(regression_model,[9000,9000,8500],enum_map)

#Fruits
scikit_perdict(regression_model,[300,"Yellow"],enum_map)

#Fruits