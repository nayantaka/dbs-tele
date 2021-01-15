user_create_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['name', 'username', 'email', 'password']
}

user_update_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    }
}
