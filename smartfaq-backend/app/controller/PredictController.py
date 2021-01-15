from app.service.IntentClassifier.Preprocessing import Embedding, Stemmer
from app.service.IntentClassifier.Model import Model
from app.service.IntentClassifier.Predict import Predict
from app.model.dataset import Dataset
from app.model.response import Response
import pandas as pd
from app import app
from app import responses as res
from app.middleware.checkapikey import apikey
from app import db
import sys
import random

if (db.engine.dialect.has_table(db.engine, 'dataset')):
	df = pd.read_sql(Dataset.query.statement, Dataset.query.session.bind)
	embed = Embedding(df['paragraph'].values, label=df['intent'], clean_text=True)
	predict = Predict()

@apikey
def index(sentence):
		result = {}
		result = predict.predict(sentence)

		if result is None:
			result['intent'] = 'unknown'

		response = Response.query.filter(Response.intent == result['intent']).all()

		if not response:
			result['response'] = 'Maaf jawaban belum tersedia'
		else:
			result['response'] = random.choice(response).response

		data = singleTransform(result)

		return res.ok(data, 'success')

def transform(res):
	array = []
	for i in res:
		array.append(singleTransform(i))

	return array

def singleTransform(response):
    data = {
        'sentence': response['sentence'],
        'intent': response['intent'],
        'response': response['response'],
        'score': response['score']
    }

    return data
