NAME_PATTERN = '[A-Za-z]{2,25}'
CONTACT_PATTERN = '^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'
TRUE = True
FALSE = False
USER = 'user'
MESSAGE = 'message'
USER_RESPONSE = 'No user found for this id'
USER_LIST_RESPONSE = 'No data found for the users'
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