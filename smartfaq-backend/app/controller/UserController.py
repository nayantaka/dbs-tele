import sys
from flask import request
from app.model.user import User
from flask_jwt_extended import *
from app import app, db, responses
from app.exception.NotFoundException import NotFoundException
from app.exception.DuplicateException import DuplicateException

@jwt_required
def index():
    current_user = get_jwt_identity()
    users = User.query
    page = 1
    per_page = 50

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))

    if request.args.get('per_page') is not None:
        per_page = int(request.args.get('per_page'))

    if request.args.get('name') is not None:
        users = users.filter(User.name.like("%{}%".format(request.args.get('name'))))

    if request.args.get('username') is not None:
        users = users.filter(User.username.like("%{}%".format(request.args.get('username'))))

    if request.args.get('email') is not None:
        users = users.filter(User.email.like("%{}%".format(request.args.get('email'))))

    users = users.paginate(page, per_page, error_out=False)
    if len(users.items) < 1 == True:
        raise NotFoundException("user not found")

    data = transform(users)

    return responses.ok(data, 'success')

def store():
    name = request.json['name']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    is_exist = User.query.filter_by(username=username).first()
    if is_exist:
        raise DuplicateException('username or email already exist')

    user = User(name=name, username=username, email=email)
    user.setPassword(password)

    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username=username).first()
    data = singleTransform(user)
    return responses.created(data, 'User successfully created')

@jwt_required
def show(id):
    users = User.query.filter_by(id=id).first()
    if not users:
        raise NotFoundException("user with id {} not found".format(id))

    data = singleTransform(users)
    return responses.ok(data, "user found")

@jwt_required
def update(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        raise NotFoundException("user with id {} not found".format(id))

    if 'email' in request.json:
        user.email = request.json['email']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'password' in request.json:
        user.setPassword(request.json['password'])

    db.session.commit()

    data = singleTransform(user)

    return responses.ok(data, 'Successfully update data!')

@jwt_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        raise NotFoundException("user with id {} not found".format(id))

    db.session.delete(user)
    db.session.commit()

    data = singleTransform(user)
    return responses.ok(data, 'Successfully delete data!')

def transform(users):
	array = []
	for i in users.items:
		array.append(singleTransform(i))

	return {
        'data': array,
        'pagination': {
            'current_page': users.page,
            'next_page': users.next_num,
            'prev_page': users.prev_num,
            'total_page': users.pages,
            'total_record': users.total,
            'per_page': users.per_page
        }
    }

def singleTransform(users):
    data = {
        'id': users.id,
        'name': users.name,
        'username': users.username,
        'email': users.email
    }

    return data
