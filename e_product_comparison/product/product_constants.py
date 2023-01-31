TRUE = True
FALSE = False
PRODUCT = 'product'
PRODUCT_RESPONSE = 'No product found for this id'
PRODUCT_LIST_RESPONSE = 'No data found for products'
ERROR_FORMAT = "'([^']*)'"

PRODUCT_SCHEMA = {
    'name': 'product',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'category_type': {'enum': ['mobile', 'laptop', 'tv']},
        'specification': {
            'name': 'specification',
            'properties': {
                'color': {'type': 'string'},
                'storage': {'type': 'string'}
            },
            'required': ['color', 'storage']
        }
    },
    'required': ['name', 'description', 'category_type', 'specification'],
    'additionalProperties': False
}



