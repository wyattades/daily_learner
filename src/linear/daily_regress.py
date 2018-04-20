from __future__ import division
import numpy as np
import random
from sklearn.preprocessing import normalize
"""
    Leo Neat #1452487
    CMPS183 Spring 2018
    Daily Learner Project Backend

    This is used as a tool kit to preform a linear regression on input data corresponding to peoples days
    The regression uses the Singular Value Decomposition Technique, and is simpler but less effective
    than the black box technique.
"""

TEST_DATA_BASE = "/mnt/FireCuda/Documents/School/Spring_2018/CMPS183/project/daily_learner/src/linear/sampledb.txt"


def gen_test_data(test_data_file):
    # Generates testable data
    with open(test_data_file, 'w+') as f:
        for i in range(0,10000):
            f.write(str(random.randint(1,3)) + " " + str(random.randint(1,3)) +" "+ str(random.randint(4,6))+ " "+
                    str(random.randint(1,2)) + " " + str(random.randint(6,10)) + " "+ str(random.randint(7,10))+ " "
                    + str(random.randint(1,2)) + " " + str(random.randint(1,2)) + " " + str(random.randint(1,5)) + " "
                    + str(random.randint(1,5)) + " 1\n")


def load_test_data(test_data_file):
    # test_data_file<String> = The location of the text file where the training data is stored
    # Training data should be stored with 11 space separated characters, the last one being the result
    # Returns [List of indexed test data, List of indexed results]

    test_data = []
    test_results = []
    with open(test_data_file) as f:
        for line in f:
            split_line = line.strip("\n")
            split_line = split_line.split(" ")
            test_results.append(split_line[-1])
            test_data.append(split_line[:-1])
    return test_data,test_results


def gen_svd_matrix(test_data, test_results):
    A = np.stack(test_data, 0)
    B = np.stack(test_results, 0)
    ls = np.linalg.lstsq(A, B, -1)
    norm_data = norm(ls[0])
    print(norm_data)

def norm(arr):
    v_bar = 0
    for i in arr:
        v_bar = v_bar + i**2
    new_arr = []
    v_bar = v_bar **(1.0/2.0)
    print(v_bar)
    for i in arr:
        new_arr.append((i/v_bar)*10)
    return new_arr

#gen_test_data(TEST_DATA_BASE)
[data,results] = load_test_data(TEST_DATA_BASE)
gen_svd_matrix(data,results)
