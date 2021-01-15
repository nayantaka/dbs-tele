import time
import threading
from app import db
import pandas as pd
from app.model.dataset import Dataset
from app.service.IntentClassifier.Model import Model
from app.service.IntentClassifier.Preprocessing import Embedding, Stemmer

class TrainModel (object):
    result = None
    def __init__(self):
        thread = threading.Thread(target=self.train, args=())
        thread.daemon = True
        thread.start()

    def train(self):
        if (db.engine.dialect.has_table(db.engine, 'dataset')):
            df = pd.read_sql(Dataset.query.statement, Dataset.query.session.bind)
            dataset = Embedding(df['paragraph'].values, label=df['intent'], clean_text=True)
            dataX = dataset.corpus_to_sequence(dataset.sentence)
            dataY = df['intent']
            model = Model(dataX, dataY, 1000, 128)
            res = model.train_model()
            self.result = res
            return res
