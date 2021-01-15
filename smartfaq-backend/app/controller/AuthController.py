import sys
import datetime
from flask import request
from app.model.user import User
from app import app, db, responses
from app.exception.PasswordNotMatch import PasswordNotMatch
from app.exception.NotFoundException import NotFoundException
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity


def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFoundException("username {} not exists".format(username))

    if not user.checkPassword(password):
        raise PasswordNotMatch("password didn't match")

    data = singleTransform(user)
    expires = datetime.timedelta(days=1)
    print(expires, file=sys.stdout)
    expires_refresh = datetime.timedelta(days=3)
    access_token = create_access_token(
        data, fresh=False, expires_delta=expires)
    refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

    return responses.ok({
        'data': data,
        'access_token': access_token,
        'refresh_token': refresh_token
    }, "successfully logged in")


@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    expires_refresh = datetime.timedelta(days=3)
    new_token = create_access_token(identity=user, fresh=False)
    refresh_token = create_refresh_token(user, expires_delta=expires_refresh)

    return responses.ok({
        "access_token": new_token
    }, "successfully update access token")


def singleTransform(users):
    data = {
        'id': users.id,
        'name': users.name,
        'username': users.username,
        'email': users.email
    }

    return data
