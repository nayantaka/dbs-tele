import sys
from flask import request
from flask_jwt_extended import *
from app import app, db, responses
from app.model.dataset import Dataset
from app.exception.NotFoundException import NotFoundException
from app.exception.DuplicateException import DuplicateException

@jwt_required
def index():
    current_dataset = get_jwt_identity()
    datasets = Dataset.query
    page = 1
    per_page = 50

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))

    if request.args.get('per_page') is not None:
        per_page = int(request.args.get('per_page'))

    if request.args.get('context') is not None:
        datasets = datasets.filter(Dataset.context.like("%{}%".format(request.args.get('context'))))

    if request.args.get('intent') is not None:
        datasets = datasets.filter(Dataset.intent.like("%{}%".format(request.args.get('intent'))))

    if request.args.get('paragraph') is not None:
        datasets = datasets.filter(Dataset.paragraph.like("%{}%".format(request.args.get('paragraph'))))

    datasets = datasets.paginate(page, per_page, error_out=False)

    if len(datasets.items) < 1 == True:
        raise NotFoundException("dataset not found")

    data = transform(datasets)

    return responses.ok(data, 'success')

@jwt_required
def store():
    context = 'nocontext'
    intent = request.json['intent']
    paragraph = request.json['paragraph']

    if 'context' in request.json:
        context = request.json['context']

    dataset = Dataset(context=context, intent=intent, paragraph=paragraph)

    db.session.add(dataset)
    db.session.commit()

    data = singleTransform(dataset)

    return responses.created(data, 'Dataset successfully created')

@jwt_required
def show(id):
    datasets = Dataset.query.filter_by(id=id).first()
    if not datasets:
        raise NotFoundException("dataset with id {} not found".format(id))

    data = singleTransform(datasets)
    return responses.ok(data, "dataset found")

@jwt_required
def update(id):
    dataset = Dataset.query.filter_by(id=id).first()
    if not dataset:
        raise NotFoundException("dataset with id {} not found".format(id))

    if 'context' in request.json:
        dataset.context = request.json['context']
    if 'intent' in request.json:
        dataset.intent = request.json['intent']
    if 'paragraph' in request.json:
        dataset.paragraph = request.json['paragraph']

    db.session.commit()

    data = singleTransform(dataset)

    return responses.ok(data, 'Successfully update data!')

@jwt_required
def delete(id):
    dataset = Dataset.query.filter_by(id=id).first()
    if not dataset:
        raise NotFoundException("dataset with id {} not found".format(id))

    db.session.delete(dataset)
    db.session.commit()

    data = singleTransform(dataset)
    return responses.ok(data, 'Successfully delete data!')

def getCategory():
    category = Dataset.query.with_entities(Dataset.intent).distinct().all()
    category = [row[0] for row in category]

    return responses.ok(category, 'Successfully get dataset category')

def transform(datasets):
	array = []
	for i in datasets.items:
		array.append(singleTransform(i))

	return {
        'data': array,
        'pagination': {
            'current_page': datasets.page,
            'next_page': datasets.next_num,
            'prev_page': datasets.prev_num,
            'total_page': datasets.pages,
            'total_record': datasets.total,
            'per_page': datasets.per_page
        }
    }

def singleTransform(datasets):
    data = {
        'id': datasets.id,
        'context': datasets.context,
        'intent': datasets.intent,
        'paragraph': datasets.paragraph
    }

    return data
