import sys
from flask import request
from app import responses
from functools import wraps
from app.model.apikey import Apikey
from app.exception.ApikeyException import ApikeyException
from app.exception.NotFoundException import NotFoundException

def apikey(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if (request.headers.get('x-api-key') is None):
            raise ApikeyException("apikey is not provided")

        is_exist = Apikey.query.filter(Apikey.key == request.headers.get('x-api-key')).count()

        if (is_exist < 1):
            raise NotFoundException("Invalid or inactive API Key")

        return f(*args, **kwargs)
    return wrapper
