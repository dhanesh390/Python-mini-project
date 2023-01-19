from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class DataNotFoundException(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'No data found'


class InvalidInput(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Invalid input, Enter again'


class InvalidValueException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'
    message = 'Invalid '

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


class AlreadyExistException(APIException):
    status_code = status.HTTP_208_ALREADY_REPORTED
    default_detail = _('Invalid input.')
    default_code = 'invalid'
    message = 'Invalid '

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)
