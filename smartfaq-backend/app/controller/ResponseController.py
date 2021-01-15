import sys
from app import app, db
from flask import request
from flask_jwt_extended import *
from app import responses as res
from app.model.dataset import Dataset
from app.model.response import Response
from app.exception.NotFoundException import NotFoundException
from app.exception.DuplicateException import DuplicateException

@jwt_required
def index():
    current_response = get_jwt_identity()
    response = Response.query
    page = 1
    per_page = 50

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))

    if request.args.get('per_page') is not None:
        per_page = int(request.args.get('per_page'))

    if request.args.get('response') is not None:
        response = response.filter(Response.response.like("%{}%".format(request.args.get('response'))))

    if request.args.get('intent') is not None:
        response = response.filter(Response.intent.like("%{}%".format(request.args.get('intent'))))

    response = response.paginate(page, per_page, error_out=False)

    if len(response.items) < 1 == True:
        raise NotFoundException("response not found")

    data = transform(response)

    return res.ok(data, 'success')

@jwt_required
def store():
    response = request.json['response']
    intent = request.json['intent']

    response = Response(response=response, intent=intent)

    db.session.add(response)
    db.session.commit()

    data = singleTransform(response)

    return res.created(data, 'Response successfully created')

@jwt_required
def show(id):
    response = Response.query.filter_by(id=id).first()
    if not response:
        raise NotFoundException("response with id {} not found".format(id))

    data = singleTransform(response)
    return res.ok(data, "response found")

@jwt_required
def update(id):
    response = Response.query.filter_by(id=id).first()
    if not response:
        raise NotFoundException("dataset with id {} not found".format(id))

    if 'response' in request.json:
        response.response = request.json['response']
    if 'intent' in request.json:
        response.intent = request.json['intent']

    db.session.commit()

    data = singleTransform(response)

    return res.ok(data, 'Successfully update data!')

@jwt_required
def delete(id):
    response = Response.query.filter_by(id=id).first()
    if not response:
        raise NotFoundException("dataset with id {} not found".format(id))

    db.session.delete(response)
    db.session.commit()

    data = singleTransform(response)
    return res.ok(data, 'Successfully delete data!')

def getCategory():
    category = Dataset.query.with_entities(Dataset.intent).distinct().all()
    category = [row[0] for row in category]

    return res.ok(category, 'Successfully get response category')

def transform(response):
	array = []
	for i in response.items:
		array.append(singleTransform(i))

	return {
        'data': array,
        'pagination': {
            'current_page': response.page,
            'next_page': response.next_num,
            'prev_page': response.prev_num,
            'total_page': response.pages,
            'total_record': response.total,
            'per_page': response.per_page
        }
    }

def singleTransform(response):
    data = {
        'id': response.id,
        'response': response.response,
        'intent': response.intent
    }

    return data
