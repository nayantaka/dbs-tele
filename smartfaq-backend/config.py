import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = os.environ.get('DEBUG')
	SECRET_KEY = os.environ.get('SECRET_KEY')

	JWT_SECRET_KEY = str(os.environ.get('JWT_SECRET'))
	
	HOST = str(os.environ.get('DB_HOST'))
	PORT = os.environ.get('DB_PORT')
	DATABASE = os.environ.get('DB_DATABASE')
	USERNAME = os.environ.get('DB_USERNAME')
	PASSWORD = os.environ.get('DB_PASSWORD')

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_RECORD_QUERIES = True