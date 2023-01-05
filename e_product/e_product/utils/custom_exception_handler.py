from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from datetime import datetime


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class AccountAlreadyExistsException(BaseCustomException):

    def __init__(self):
        detail = "Notification email has already used with the customer type"
        super().__init__(detail, status.HTTP_409_CONFLICT)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['message'] = response.data['detail']
        response.data['time'] = datetime.now()
        del response.data['detail']
    return response
