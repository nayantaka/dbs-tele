from app.model.user import User
import os
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
        # Jangan hardcode kredensial. Baca dari env; fallback acak jika tidak diset.
        password = os.environ.get('SEED_ADMIN_PASSWORD')
        if not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            print("SEED_ADMIN_PASSWORD not set; generated temporary password:", password)

        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=User,
            init={
                "name": os.environ.get('SEED_ADMIN_NAME', 'admin'),
                "username": os.environ.get('SEED_ADMIN_USERNAME', 'admin'),
                "email": os.environ.get('SEED_ADMIN_EMAIL', 'admin@admin.com'),
                "password": password
            }
        )

        # Create 1 user
        for user in faker.create(1):
            print("Adding user: %s" % user)
            self.db.session.add(user)
