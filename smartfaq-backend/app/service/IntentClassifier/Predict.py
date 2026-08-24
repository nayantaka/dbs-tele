import json
import numpy as np
import tensorflow as tf
from app.service.IntentClassifier.Preprocessing import Embedding, Stemmer

class Predict:
	def __init__(self):
		self.ERROR_THRESHOLD = 0.75
		with open("data-rnn-lstm.json", "r", encoding="utf-8") as f:
			self.data = json.load(f)
		self.label = {int(k): v for k, v in self.data['intent'].items()}
		self.model = tf.keras.models.load_model('./model-rnn-lstm.h5')
		self.embedder = Embedding(self.data['sentence'], clean_text=False)

	def predict(self, sentence):
		sentence_pad = self.embedder.text_to_sequence(sentence)
		pred = self.model.predict(sentence_pad)
		pred = [[i,r] for i,r in enumerate(pred[0]) if r > self.ERROR_THRESHOLD]
		pred.sort(key = lambda x: x[1], reverse = True)
		intent = 'unknown'
		score = -1
		if len(pred) > 0:
			score = float('{:0.4f}'.format(pred[0][1]))
			intent = self.label[int(pred[0][0])]

		return {
			'sentence': sentence,
			'score': score,
			'intent': intent
		}