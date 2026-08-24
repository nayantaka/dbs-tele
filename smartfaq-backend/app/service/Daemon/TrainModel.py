import time
import threading
from app import db
import pandas as pd
from app.model.dataset import Dataset
from app.service.IntentClassifier.Model import Model
from app.service.IntentClassifier.Preprocessing import Embedding, Stemmer
from app.exception.DuplicateException import DuplicateException

_training_lock = threading.Lock()
_training_in_progress = False

class TrainModel (object):
    result = None
    def __init__(self):
        global _training_in_progress
        with _training_lock:
            if _training_in_progress:
                raise DuplicateException("training is already in progress")
            _training_in_progress = True

        thread = threading.Thread(target=self.train, args=())
        thread.daemon = True
        thread.start()

    def train(self):
        global _training_in_progress
        try:
            if (db.engine.dialect.has_table(db.engine, 'dataset')):
                df = pd.read_sql(Dataset.query.statement, Dataset.query.session.bind)
                dataset = Embedding(df['paragraph'].values, label=df['intent'], clean_text=True)
                dataX = dataset.corpus_to_sequence(dataset.sentence)
                dataY = df['intent']
                model = Model(dataX, dataY, 1000, 128)
                res = model.train_model()
                self.result = res
                return res
        finally:
            with _training_lock:
                _training_in_progress = False