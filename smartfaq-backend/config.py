import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = os.environ.get('DEBUG')
	SECRET_KEY = os.environ.get('SECRET_KEY')

	JWT_SECRET_KEY = str(os.environ.get('JWT_SECRET'))

	# Token disimpan di HttpOnly cookie agar XSS tidak bisa mencuri kredensial.
	# Header tetap diizinkan agar tidak memutus integrasi yang memakai Authorization.
	JWT_TOKEN_LOCATION = ['headers', 'cookies']
	JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
	JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
	JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE', 'false').lower() == 'true'
	JWT_COOKIE_CSRF_PROTECT = os.environ.get('JWT_COOKIE_CSRF_PROTECT', 'true').lower() == 'true'
	JWT_COOKIE_SAMESITE = 'Lax'
	JWT_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
	JWT_ACCESS_CSRF_COOKIE_NAME = 'csrf_access_token'
	JWT_REFRESH_CSRF_COOKIE_NAME = 'csrf_refresh_token'
	JWT_ACCESS_COOKIE_PATH = '/'
	JWT_REFRESH_COOKIE_PATH = '/auth/refresh'
	JWT_SESSION_COOKIE = False

	CORS_ORIGINS = [o.strip() for o in os.environ.get(
		'CORS_ORIGINS', 'http://localhost:3000,http://localhost:8080').split(',') if o.strip()]
	
	HOST = str(os.environ.get('DB_HOST'))
	PORT = os.environ.get('DB_PORT')
	DATABASE = os.environ.get('DB_DATABASE')
	USERNAME = os.environ.get('DB_USERNAME')
	PASSWORD = os.environ.get('DB_PASSWORD')

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_RECORD_QUERIES = True