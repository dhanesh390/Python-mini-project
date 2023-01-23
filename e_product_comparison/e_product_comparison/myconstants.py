NAME_PATTERN = '[A-Za-z]{2,25}'
CONTACT_PATTERN = '^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'
USER = 'user'
SHOP = 'shop'
PRODUCT = 'product'
OFFER = 'offer'
MESSAGE = 'message'
USER_RESPONSE = 'No user found for this id'
PRODUCT_RESPONSE = 'No product found for this id'
SHOP_RESPONSE = 'No shop found for this id'
OFFER_RESPONSE = 'No offer found for this id'
USER_LIST_RESPONSE = 'No data found for the users'
PRODUCT_LIST_RESPONSE = 'No data found for products'
SHOP_LIST_RESPONSE = 'No data found for shops'
OFFER_LIST_RESPONSE = 'No data found for offers'
TRUE = True
FALSE = False

USER_SCHEMA = {
    'name': 'user',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'contact_number': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'user_role': {'type': 'string'},
        'is_seller': {'enum': [True, False]}
    },
    'required': ['first_name', 'last_name', 'username', 'password', 'contact_number', 'email', 'user_role', 'is_seller']
}


SHOP_SCHEMA = {
    'name': 'shop',
    'properties': {
        'name': {'type': 'string'},
        'contact_number': {'type': 'string'},
        'building_no': {'type': 'string'},
        'street_name': {'type': 'string'},
        'locality': {'type': 'string'},
        'district': {'type': 'string'},
        'state': {'type': 'string'},
        'country': {'type': 'string'},
        'pincode': {'type': 'string'}
    },
    'required': ['name', 'contact_number', 'building_no', 'street_name', 'locality', 'district', 'state',
                 'country', 'pincode']
}

PRODUCT_SCHEMA = {
    'name': 'product',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'category_type': {'enum': ['mobile', 'laptop', 'tv']},
        'specification': {
            'type': 'object',
            'properties': {
                'color': {'type': 'string'},
                'storage': {'type': 'string'}
            }
        }
    },
    'required': ['name', 'description', 'category_type', 'specification']
}
