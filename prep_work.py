#Original file is located at: https://colab.research.google.com/drive/1AUofaupklsbrcfQlN5HKs8n2Rvwaq9wF

import requests
import numpy as np
import ast
import tensorflow as tf
from sklearn.model_selection import train_test_split

#Import and process the data into numpy arrays:

url_WP4s = 'https://raw.githubusercontent.com/TomasSilva/MLcCY7/main/Data/WP4s.txt'
url_WP4_Hodges = 'https://raw.githubusercontent.com/TomasSilva/MLcCY7/main/Data/WP4_Hodges.txt'

#dataset 1:
WP4_Hodges_raw = requests.get(url_WP4_Hodges) #opens the file

WP4_Hodges_list = ast.literal_eval(WP4_Hodges_raw.text) #converts from string to list
WP4_Hodges = np.array(WP4_Hodges_list) #converts from list to NumPy array

#dataset 2:
WP4s_raw = requests.get(url_WP4s) #opens the file

WP4s_list = ast.literal_eval(WP4s_raw.text) #converts from string to list
WP4s = np.array(WP4s_list) #converts from list to NumPy array

print("shape of WP4s: " + str(WP4s.shape))
print("shape of WP4_Hodges: " + str(WP4_Hodges.shape))

#Define and train neural network:

X = WP4s
y = WP4_Hodges
X_train, X_test, y_train, y_test = train_test_split(WP4s, y, test_size=0.5) #split data into training and testing
X_train, X_test = tf.keras.utils.normalize(X_train, axis=1), tf.keras.utils.normalize(X_test, axis=1) #normalise

def get_network():
    inp = tf.keras.layers.Input(shape=(5,))
    prep = tf.keras.layers.Flatten()(inp)
    h1 = tf.keras.layers.Dense(1000, activation=tf.nn.relu)(prep)
    h2 = tf.keras.layers.Dense(100, activation=tf.nn.relu)(h1)
    out = tf.keras.layers.Dense(2, activation=tf.nn.relu)(h2)

    model = tf.keras.models.Model(inputs=inp, outputs=out)
    model.compile(
        loss='mean_squared_error',
        optimizer=tf.keras.optimizers.Adam(0.001),
        metrics = ['accuracy']
    )
    return model

def train_network(X_train, y_train, X_test, y_test):
    model = get_network()
    history = model.fit(
        X_train, y_train,
        epochs=20,
        validation_data=(X_test, y_test),
    )
    return history

model = get_network()
print(model.summary())

history = train_network(X_train, y_train, X_test, y_test)
