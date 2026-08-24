import sys
import datetime
from flask import request
from app.model.user import User
from app import app, db, responses
from app.exception.PasswordNotMatch import PasswordNotMatch
from app.exception.NotFoundException import NotFoundException
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)


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
    expires_refresh = datetime.timedelta(days=3)
    access_token = create_access_token(
        data, fresh=False, expires_delta=expires)
    refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

    resp = responses.ok({'data': data}, "successfully logged in")
    # Token disimpan di HttpOnly cookie (ada header CSRF terpisah), bukan di body
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp


@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    expires_refresh = datetime.timedelta(days=3)
    new_token = create_access_token(identity=user, fresh=False)
    refresh_token = create_refresh_token(user, expires_delta=expires_refresh)

    resp = responses.ok({}, "successfully update access token")
    set_access_cookies(resp, new_token)
    set_refresh_cookies(resp, refresh_token)

    return resp


def logout():
    resp = responses.ok({}, "successfully logged out")
    unset_jwt_cookies(resp)
    return resp


def singleTransform(users):
    data = {
        'id': users.id,
        'name': users.name,
        'username': users.username,
        'email': users.email
    }

    return data
