TRUE = True
FALSE = False
MESSAGE = 'message'
SHOP = 'shop'
SHOP_RESPONSE = 'No shop found for this id'
SHOP_LIST_RESPONSE = 'No data found for shops'
ERROR_PATTERN = "'([^']*)'"
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
                 'country', 'pincode'],
    'additionalProperties': False
}
