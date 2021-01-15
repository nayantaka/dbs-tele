import secrets
from app import db
from datetime import datetime
from app.model.user import User

class Apikey(db.Model):
	id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
	key = db.Column(db.String(125), nullable = False)
	user_id = db.Column(db.BigInteger, db.ForeignKey(User.id))
	created_at = db.Column(db.DateTime, default = datetime.utcnow)
	updated_at = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Apikey {}>'.format(self.key)

	def generateKey(self):
		self.key = secrets.token_urlsafe(64)