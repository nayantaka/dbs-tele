from app.model.user import User
import random
import string
from flask_seeder import Seeder, Faker, generator
from werkzeug.security import generate_password_hash

# SQLAlchemy database model


class User(User):
    def __init__(self, name=None, username=None, email=None, password=None):
        self.name = name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __str__(self):
        return "Name=%s, Email=%s, Password=%s" % (self.name, self.email, self.password)

# All seeders inherit from Seeder


class UserSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=User,
            init={
                "name": 'admin',
                "username": 'admin',
                "email": 'admin@admin.com',
                "password": "secret"
            }
        )

        # Create 1 user
        for user in faker.create(1):
            print("Adding user: %s" % user)
            self.db.session.add(user)
