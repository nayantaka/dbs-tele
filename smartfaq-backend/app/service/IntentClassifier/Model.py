import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation, Dropout, Embedding, Bidirectional
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
import pandas as pd
import random

class Model:
	def __init__(self, dataX, dataY, max_nb_words = 1000, embedding_dim = 128):
		self.dataX = dataX
		self.dataY = dataY
		self.MAX_NB_WORDS = int(max_nb_words)
		self.EMBEDDING_DIM = int(embedding_dim)

	def train_model(self):
		X = self.dataX
		Y = pd.get_dummies(self.dataY).values
		X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.10, random_state = 58)

		model = Sequential()
		model.add(Embedding(int(self.MAX_NB_WORDS), int(self.EMBEDDING_DIM), input_length = X.shape[1]))
		model.add(Dropout(0.25))
		model.add(LSTM(int(self.EMBEDDING_DIM/2), dropout=0.25, recurrent_dropout=0.25))
		# for bidirectional lstm (bi-lstm) use this below layer
		# model.add(Bidirectional(LSTM(64, dropout=0.25, recurrent_dropout=0.25)))
		model.add(Dense(len(Y[1]), activation='softmax'))
		model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

		model.fit(X_train, Y_train, epochs=250, batch_size=5, verbose=1)

		acc = model.evaluate(X_test, Y_test)

		model.save('./model-rnn-lstm.h5')

		print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(acc[0], acc[1]))

		return True