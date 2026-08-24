response_create_schema = {
    'type': 'object',
    'properties': {
        'response': {'type': 'string'},
        'intent': {'type': 'string', 'maxLength': 25}
    },
    'required': ['response', 'intent']
}

response_update_schema = {
    'type': 'object',
    'properties': {
        'response': {'type': 'string'},
        'intent': {'type': 'string', 'maxLength': 25}
    }
}