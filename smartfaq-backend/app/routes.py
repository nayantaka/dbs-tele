from app import app
from flask import request
from app.controller import UserController
from app.controller import PredictController
from app.controller import AuthController
from app.controller import ApikeyController
from app.controller import DatasetController
from app.controller import ResponseController
from app.controller import TrainController
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required
from app.middleware.ratelimit import rate_limit

from app.schema import UserSchema
from app.schema import DatasetSchema
from app.schema import ResponseSchema

@app.route('/auth/login', methods=['POST'])
@rate_limit(limit=10, window=60, key_func=lambda: request.remote_addr)
def login():
	return AuthController.login()

@app.route('/auth/register', methods=['POST'])
@expects_json(UserSchema.user_create_schema)
def register():
	return UserController.store()

@app.route('/auth/refresh', methods=['POST'])
def refresh():
    return AuthController.refresh()

@app.route('/auth/logout', methods=['POST'])
def logout():
    return AuthController.logout()

@app.route('/dataset/category', methods=['GET'])
@jwt_required
def datasetCategory():
	return DatasetController.getCategory()

@app.route('/dataset', methods=['GET', 'POST'])
@expects_json(DatasetSchema.dataset_create_schema, ignore_for=['GET'])
def datasets():
	if request.method == 'GET':
		return DatasetController.index()
	if request.method == 'POST':
		return DatasetController.store()

@app.route('/dataset/<id>', methods=['PUT', 'GET', 'DELETE'])
@expects_json(DatasetSchema.dataset_update_schema, ignore_for=['GET', 'DELETE'])
def datasetDetail(id):
	if request.method == 'GET':
  		return DatasetController.show(id)
	if request.method == 'PUT':
		return DatasetController.update(id)
	if request.method == 'DELETE':
		return DatasetController.delete(id)

@app.route('/response/category', methods=['GET'])
@jwt_required
def responseCategory():
	return ResponseController.getCategory()

@app.route('/response', methods=['GET', 'POST'])
@expects_json(ResponseSchema.response_create_schema, ignore_for=['GET'])
def response():
	if request.method == 'GET':
		return ResponseController.index()
	if request.method == 'POST':
		return ResponseController.store()

@app.route('/response/<id>', methods=['PUT', 'GET', 'DELETE'])
@expects_json(ResponseSchema.response_update_schema, ignore_for=['GET', 'DELETE'])
def responseDetail(id):
	if request.method == 'GET':
  		return ResponseController.show(id)
	if request.method == 'PUT':
		return ResponseController.update(id)
	if request.method == 'DELETE':
		return ResponseController.delete(id)

@app.route('/user', methods=['GET', 'POST'])
@expects_json(UserSchema.user_create_schema, ignore_for=['GET'])
@jwt_required
def users():
	if request.method == 'GET':
		return UserController.index()
	if request.method == 'POST':
		return UserController.store()

@app.route('/user/<id>', methods=['PUT', 'GET', 'DELETE'])
@expects_json(UserSchema.user_update_schema, ignore_for=['GET', 'DELETE'])
def usersDetail(id):
	if request.method == 'GET':
  		return UserController.show(id)
	if request.method == 'PUT':
		return UserController.update(id)
	if request.method == 'DELETE':
		return UserController.delete(id)

@app.route('/apikey', methods=['GET', 'POST'])
def apis():
	if request.method == 'GET':
		return ApikeyController.index()
	if request.method == 'POST':
		return ApikeyController.store()

@app.route('/apikey/<id>', methods=['PUT', 'GET', 'DELETE'])
def apiDetail(id):
	if request.method == 'GET':
  		return ApikeyController.show(id)
	if request.method == 'PUT':
		return ApikeyController.update(id)
	if request.method == 'DELETE':
		return ApikeyController.delete(id)

@app.route('/predict')
@rate_limit(limit=120, window=60, key_func=lambda: request.headers.get('x-api-key', request.remote_addr))
def index():
	sentence = request.args.get('sentence')
	return PredictController.index(sentence)

@app.route('/train', methods=['POST'])
def train():
	return TrainController.index()
