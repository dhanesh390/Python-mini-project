NAME_PATTERN = '[A-Za-z]{2,25}'
CONTACT_PATTERN = '^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'
MESSAGE = 'message'
USER_RESPONSE = 'No data found for the users'
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


# validate_value = Validator({
#     'first_name': {'type': 'string', 'required': True},
#     'last_name': {'type': 'string', 'required': True},
#     'username': {'type': 'string', 'required': True},
#     'password': {'type': 'string', 'required': True},
#     'contact_number': {'type': 'string', 'required': True},
#     'email': {'type': 'string', 'format': 'email', 'required': True},
#     'user_role': {'type': 'string', 'required': True},
#     'is_seller': {'enum': [True, False], 'required': False}})
# print('1: ', validate_value.validate(request.data))