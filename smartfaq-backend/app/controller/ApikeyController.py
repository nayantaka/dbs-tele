import sys
from flask import request
from app.model.apikey import Apikey
from app import app, db, responses
from flask_jwt_extended import *
from app.exception.NotFoundException import NotFoundException
from app.exception.DuplicateException import DuplicateException

@jwt_required
def index():
    current_user = get_jwt_identity()
    page = 1
    per_page = 50
    apis = Apikey.query

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))

    if request.args.get('per_page') is not None:
        per_page = int(request.args.get('per_page'))

    if (current_user['id'] is not None):
        apis = apis.filter(Apikey.user_id == current_user['id'])

    apis = apis.paginate(page, per_page, error_out=False)

    if len(apis.items) < 1 == True:
        raise NotFoundException("api key not found")

    data = transform(apis)
    return responses.ok(data, 'success')

@jwt_required
def store():
    current_user = get_jwt_identity()

    api = Apikey(user_id=current_user['id'])
    api.generateKey()

    is_exist = Apikey.query.filter_by(key=api.key).first()

    if is_exist:
        raise DuplicateException("api key {} is already exists".format(api.key))

    db.session.add(api)
    db.session.commit()

    api = Apikey.query.filter_by(key=api.key).first()
    data = singleTransform(api)

    return responses.created(data, 'Apikey successfully created')

@jwt_required
def show(id):
    api = Apikey.query.filter_by(id=id).first()
    if not api:
        raise NotFoundException("api key with id {} is not found".format(id))

    data = singleTransform(api)

    return responses.ok(data, "api key found")

@jwt_required
def update(id):
    api = Apikey.query.filter_by(id=id).first()
    if not api:
        raise NotFoundException("api key with id {} is not found".format(id))

    api.generateKey()
    db.session.commit()

    data = singleTransform(api)

    return responses.ok(data, 'Successfully update data!')

@jwt_required
def delete(id):
    api = Apikey.query.filter_by(id=id).first()
    if not api:
        raise NotFoundException("api key with id {} is not exist".format(id))

    db.session.delete(api)
    db.session.commit()

    data = singleTransform(api)
    return responses.ok(data, 'Successfully delete data!')

def transform(apis):
    array = []
    for i in apis.items:
        array.append(singleTransform(i))

    return {
        'data': array,
        'pagination': {
            'current_page': apis.page,
            'next_page': apis.next_num,
            'prev_page': apis.prev_num,
            'total_page': apis.pages,
            'total_record': apis.total,
            'per_page': apis.per_page
        }
    }

def singleTransform(apis):
    data = {
        'id': apis.id,
        'key': apis.key
    }

    return data
