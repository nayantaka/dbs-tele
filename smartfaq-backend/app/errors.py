import sys
from app import app
from jsonschema import ValidationError
from flask import jsonify, make_response
from app.exception.ApikeyException import ApikeyException
from app.exception.PasswordNotMatch import PasswordNotMatch
from app.exception.NotFoundException import NotFoundException
from app.exception.DuplicateException import DuplicateException

@app.errorhandler(Exception)
def server_error(err):
    print(err, file=sys.stdout)
    res = {
        'success': False,
		'message': "internal server error"
	}

    return res, 500

@app.errorhandler(NotFoundException)
def server_error(err):
    res = {
        'success': False,
		'message': err.message
	}

    return res, 404

@app.errorhandler(DuplicateException)
def server_error(err):
    res = {
        'success': False,
		'message': err.message
	}

    return res, 409

@app.errorhandler(PasswordNotMatch)
def server_error(err):
    res = {
        'success': False,
		'message': err.message
	}

    return res, 401

@app.errorhandler(ApikeyException)
def apikey(err):
    res = {
        'success': False,
		'message': err.message
	}

    return res, 400

@app.errorhandler(400)
def bad_request(err):
    if isinstance(err.description, ValidationError):
        original_error = err.description
        res = {
            'success': False,
            'message': original_error.message
        }
        return res, 400
