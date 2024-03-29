def func():
    return "hello there"


    #importing dependencies
#gudie: https://medium.com/the-handbook-of-coding-in-finance/stock-prices-prediction-using-long-short-term-memory-lstm-model-in-python-734dd1ed6827

import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def ltsm():
    df = yf.download('BTC-USD')
    df.head()

    #Data split, 80% training_data

    close_prices = df['Close']
    values = close_prices.values
    training_data_len = math.ceil(len(values)* 0.8)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(values.reshape(-1,1))
    train_data = scaled_data[0: training_data_len, :]

    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #test set 20%

    test_data = scaled_data[training_data_len-60: , : ]
    x_test = []
    y_test = values[training_data_len:]

    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    #setting up LSTM Network Architecture
    model = keras.Sequential()
    model.add(layers.LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(layers.LSTM(100, return_sequences=False))
    model.add(layers.Dense(25))
    model.add(layers.Dense(1))
    model.summary()

    #fitting training set

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size= 1, epochs=3)

    #evaluate model with test set and check performance with rmse

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    rmse = np.sqrt(np.mean(predictions - y_test)**2)
    rmse

    #visualize prediction

    data = df.filter(['Close'])
    train = data[:training_data_len]
    validation = data[training_data_len:]
    validation.loc[:, 'Predictions'] = predictions

    
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_title('Model')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price USD ($)')
    
    # Plot training data
    ax.plot(data.index[:training_data_len], train, label='Train')

    # Plot validation data and predictions
    ax.plot(data.index[training_data_len:], validation['Close'], label='Val')
    ax.plot(data.index[training_data_len:], predictions, label='Predictions')

    ax.legend(loc='lower right')

    return fig, ax
