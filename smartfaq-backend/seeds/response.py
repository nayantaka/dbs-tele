from app.model.response import Response
import random
import string
from flask_seeder import Seeder, Faker, generator
import pandas as pd
# SQLAlchemy database model


class Response(Response):
    def __init__(self, response=None, intent=None):
        self.response = response
        self.intent = intent

    def __str__(self):
        return "Intent=%" % (self.intent)

# All seeders inherit from Seeder

class DatasetSeeder(Seeder):
    # run() will be called by Flask-Seeder
    def run(self):
        datasetFile = 'response.csv'
        df = pd.read_csv(datasetFile)
        # Create a new Faker and tell it how to create User objects

        for index, respon in df.iterrows():
            res = Response(respon['response'], respon['intent'])
            self.db.session.add(res)
