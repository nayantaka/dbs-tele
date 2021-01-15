from flask import jsonify, make_response

def ok(values, message = None):
	res = {
        'success': True,
		'result': values,
		'message': message
	}

	return make_response(jsonify(res)), 200

def created(values, message = None):
    res = {
        'success': True,
		'result': values,
		'message': message
	}

    return make_response(jsonify(res)), 201
