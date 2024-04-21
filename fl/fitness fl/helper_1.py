import tensorflow as tf
import csv
import numpy as np
import os
import warnings
import random

from math import sqrt
from numpy import concatenate
import numpy as np
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

import pandas as pd
import os
import numpy as np

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

warnings.filterwarnings("ignore")

class TFML:
    def series_to_supervised(self,data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        df = DataFrame(data)
        cols, names = list(), list()
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
        agg = concat(cols, axis=1)
        agg.columns = names
        if dropnan:
            agg.dropna(inplace=True)
        return agg
    def dataProcess(self):
        path = 'data1.csv'
        dataset = read_csv(path, header=0, index_col=0)
        ColumnsName = dataset.columns.values.tolist()
        values = dataset.values
        values = values.astype('float32')
        scaled = self.scaler.fit_transform(values)

        reframed = self.series_to_supervised(scaled, 1, 1)
        # drop columns we don't want to predict
        reframed.drop(reframed.columns[[i for i in range(len(scaled[0]) + 1, 2 * len(scaled[0]))]], axis=1,
                      inplace=True)
        print(reframed.head())

        # split into train and test sets
        values = reframed.values
        n_train_hours = 6485
        train = values[:n_train_hours, :]
        test = values[n_train_hours:, :]
        # split into input and outputs
        train_X, train_y = train[:, :-1], train[:, -1]
        test_X, test_y = test[:, :-1], test[:, -1]
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
        test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        return train_X, train_y, test_X, test_y,scaled

    def __init__(self,name):
        self.name=name
        #self.look_back=1
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.train_X,self.train_y,self.test_X, self.test_y,self.dataset=self.dataProcess()
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(50, input_shape=(self.train_X.shape[1], self.train_X.shape[2])),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')



    def run(self):
        # fit network
        history = self.model.fit(self.train_X, self.train_y, epochs=10, batch_size=72, validation_data=(self.test_X, self.test_y), verbose=2,
                            shuffle=False)

    def eval(self):
        yhat = self.model.predict(self.test_X)
        yhat = yhat.reshape((-1, 1))
        test_X = self.test_X.reshape((self.test_X.shape[0], self.test_X.shape[2]))
        # invert scaling for forecast
        inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
        inv_yhat = self.scaler.inverse_transform(inv_yhat)
        inv_yhat = inv_yhat[:, 0]
        # invert scaling for actual
        test_y = self.test_y.reshape((len(self.test_y), 1))
        inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
        inv_y = self.scaler.inverse_transform(inv_y)
        inv_y = inv_y[:, 0]
        # calculate RMSE
        rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
        print('Test RMSE: %.3f' % rmse)
        print('Test NRMSE: %.3f' % (rmse / (max(inv_y) - min(inv_y))))

        x = np.arange(0, len(inv_y), 1)












