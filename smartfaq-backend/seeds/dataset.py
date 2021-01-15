from app.model.dataset import Dataset
import random
import string
from flask_seeder import Seeder, Faker, generator
from werkzeug.security import generate_password_hash
import pandas as pd
import sys
# SQLAlchemy database model


class Dataset(Dataset):
    def __init__(self, paragraph=None, intent=None, context=None):
        self.paragraph = paragraph
        self.intent = intent
        self.context = context

    def __str__(self):
        return "Intent=%" % (self.intent)

# All seeders inherit from Seeder


class DatasetSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        datasetFile = 'CSVdataset - Sheet1.csv'
        df = pd.read_csv(datasetFile)
        # Create a new Faker and tell it how to create User objects

        for index, dataset in df.iterrows():
            # print(dataset['paragraph'])
            dt = Dataset(dataset['paragraph'], dataset['intent'], 'nocontext')
            self.db.session.add(dt)
