from app import db
from datetime import datetime


class Dataset(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    paragraph = db.Column(db.Text(), nullable=False)
    intent = db.Column(db.String(25), nullable=False)
    context = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Dataset {}>'.format(self.intent)

