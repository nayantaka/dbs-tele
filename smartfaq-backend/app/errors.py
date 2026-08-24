import sys
from app import app
from jsonschema import ValidationError
from flask import jsonify, make_response
from app.exception.ApikeyException import ApikeyException
from app.exception.PasswordNotMatch import PasswordNotMatch
from app.exception.NotFoundException import NotFoundException
from app.exception.DuplicateException import DuplicateException

@app.errorhandler(Exception)
def handle_internal_error(err):
    print(err, file=sys.stdout)
    res = {
        'success': False,
		'message': "internal server error"
	}

    return make_response(jsonify(res)), 500

@app.errorhandler(NotFoundException)
def handle_not_found(err):
    res = {
        'success': False,
		'message': err.message
	}

    return make_response(jsonify(res)), 404

@app.errorhandler(DuplicateException)
def handle_duplicate(err):
    res = {
        'success': False,
		'message': err.message
	}

    return make_response(jsonify(res)), 409

@app.errorhandler(PasswordNotMatch)
def handle_password_not_match(err):
    res = {
        'success': False,
		'message': err.message
	}

    return make_response(jsonify(res)), 401

@app.errorhandler(ApikeyException)
def handle_apikey(err):
    res = {
        'success': False,
		'message': err.message
	}

    return make_response(jsonify(res)), 400

@app.errorhandler(400)
def bad_request(err):
    if isinstance(err.description, ValidationError):
        message = err.description.message
    else:
        message = getattr(err, 'description', '')
        if not isinstance(message, str) or not message:
            message = 'bad request'

    res = {
        'success': False,
        'message': message
    }

    return make_response(jsonify(res)), 400
