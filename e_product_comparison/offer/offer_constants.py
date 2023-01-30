TRUE = True
FALSE = False
MESSAGE = 'message'
ID = 'id'
NAME = 'name'
OFFER = 'offer'
COLOR = 'color'
STORAGE = 'storage'
SPECIFICATION = 'specification'
OFFER_RESPONSE = 'No offer found for this id'
OFFER_LIST_RESPONSE = 'No data found for offers'
FINDING_PRODUCT = 'finding the product of id'
PRODUCT_FOUND = 'product found for the id'
INVALID_KEY = 'Invalid value for the key '
VALUE_ERROR_PATTERN = "'([^']*)'"
USER_RESPONSE = 'No user found for this id'
PRODUCT = 'product'
PRODUCT_RESPONSE = 'No product found for this id'
PRODUCT_LIST_RESPONSE = 'No data found for products'
SHOP = 'shop'
SHOP_RESPONSE = 'No shop found for this id'
OFFER_SCHEMA = {
    'name': 'offer',
    'properties': {
        'product': {'type': 'number'},
        'shop': {'type': 'number'},
        'actual_price': {'type': 'number'},
        'offer_percentage': {'type': 'number'},
        'vendor_price': {'type': 'number'}
    },
    'required': ['product', 'shop', 'actual_price', 'offer_percentage', 'vendor_price']
}

# OFFER_SCHEMA = {
#     'name': 'offer',
#     'properties': {
#         'product': {'type': 'number'},
#         'shop': {'type': 'number'},
#         'original_price': {'type': 'number'},
#         'discount': {'type': 'number'},
#         'discount_price': {'type': 'number'}
#     },
#     'required': ['product', 'shop', 'original_price', 'discount', 'discount_price']
# }

PRODUCT_SEARCH_SCHEMA = {
    'name': 'product',
    'properties': {
        'name': {'type': 'string'},
        'specification': {
            'properties': {
                'color': {'type': 'string'},
                'storage': {'type': 'string'}
            },
            'required': ['color', 'storage']
        }
    },
    'required': ['name', 'specification']
}
