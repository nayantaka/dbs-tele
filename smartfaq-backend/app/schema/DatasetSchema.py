dataset_create_schema = {
    'type': 'object',
    'properties': {
        'context': {'type': 'string', 'maxLength': 25},
        'intent': {'type': 'string', 'maxLength': 25},
        'paragraph': {'type': 'string'}
    },
    'required': ['intent', 'paragraph']
}

dataset_update_schema = {
    'type': 'object',
    'properties': {
        'context': {'type': 'string', 'maxLength': 25},
        'intent': {'type': 'string', 'maxLength': 25},
        'paragraph': {'type': 'string'}
    }
}