import numpy as np
import pandas as pd

from itertools import repeat

import keras
from keras.models import Sequential
from keras.layers import Dense

import random

import matplotlib.pyplot as plt
from matplotlib import cm

import multiprocessing
import sys

def get_randoms(unl,num_pos,l):

    rnd = np.random.RandomState(l)

    unl_indicies = unl.index.tolist()

    unl_rand = unl.sample(n=num_pos, random_state=rnd)
    unl_rand_indicies = unl_rand.index.tolist()

    unl_rand.iloc[:,0] = 0

    unl_others = unl.drop(unl_rand_indicies)
    unl_others_indicies = unl_others.index.tolist()

    return unl_rand, unl_rand_indicies, unl_others, unl_others_indicies

def classification_model(X):
    # create model
    model = Sequential()
    model.add(Dense(10, activation='relu', input_shape=(X.shape[1],)))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # compile model
    model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.1), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train(unl,pos,X,l):
    print("Training %i/8"%l,flush=True)
    sys.stdout.flush()
    unl_rand, unl_rand_indicies, unl_others, unl_others_indicies = get_randoms(unl,pos.shape[0],l)

    dsample = pd.concat((unl_rand,pos), axis = 0)

    X = dsample.drop(['in playlist'], axis =1)
    y = dsample.iloc[:,0]

    model = classification_model(X)
    model.fit(X, y, epochs=800, verbose=0, batch_size = 10)

    X_others = unl_others.drop(['in playlist'], axis =1)
    y_others = unl_others.iloc[:,0]

    pred = model.predict(X_others,batch_size=1)

    d_counts = np.zeros(unl.shape[0], dtype=np.int64)
    d_sums = np.zeros(unl.shape[0], dtype=np.float32)

    for i in range(len(unl_others_indicies)):
        ind = unl_others_indicies
        d_counts[ind[i]] += 1
        d_sums[ind[i]] += pred[i]

    return d_sums, d_counts

def mult_pr_NN(unl,pos,X):
    l = list(range(8))
    d_counts = np.zeros(unl.shape[0], dtype=np.int64)
    d_sums = np.zeros(unl.shape[0], dtype=np.float32)

    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_count)

    d_sums_i, d_counts_i = zip(*pool.starmap(train, zip(repeat(unl),repeat(pos), repeat(X), l)))

    pool.close()
    pool.join()

    # print(d_counts_i[0])
    # print(d_counts_i[1])

    for i in range(len(l)):
        d_counts += d_counts_i[i]
        d_sums += d_sums_i[i]

    # for i in range(8):
    #     print(d_sums_i[i][0],"\t",d_counts_i[i][0])
    # print(d_sums[0],"\t",d_counts[0])

    colors = 'brg'

    p = (d_sums/d_counts).round(2)
    p = p.reshape(-1,1)
    x = list(range(p.shape[0]))

    # print(p[0])
    # print(d_sums[0]/d_counts[0])

    # print(d_counts)
    # print(d_sums)

    lo = 0.20; hi = 0.90

    plt.scatter(x,p, c=p, cmap =colors)
    plt.axhline(y=hi, color = 'lime')
    plt.axhline(y=lo, color = 'blue')
    plt.show()
    return p