from http import HTTPStatus
from typing import Any

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        http_code_to_message = {v.value: v.description for v in HTTPStatus}

        error_payload = {
            "error": {
                "status_code": 0,
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload

    return Response(response)


def custom_error_response(field: str, message: str, code) -> JsonResponse:
    error_response = {
        'error': {
            'field': '',
            'message': 'Invalid data',
            'status_code': status.HTTP_400_BAD_REQUEST
        }
    }
    error = error_response['error']
    error_status = status.HTTP_400_BAD_REQUEST
    if field:
        error['field'] = field

    if message:
        error['message'] = message

    if code == 400:
        error['status_code'] = 400
        error_status = status.HTTP_400_BAD_REQUEST
    elif code == 200:
        error['status_code'] = 200
        error_status = status.HTTP_200_OK
    elif code == 201:
        error['status_code'] = 201
        error_status = status.HTTP_201_CREATED

    response = error_response

    return JsonResponse({'error_details': response}, status=error_status)


def custom_success_response(field: str, message: str, code) -> JsonResponse:
    success_response = {
        'result': {
            'field': '',
            'message': 'No data',
            'status_code': status.HTTP_200_OK
        }
    }
    success = success_response['error']
    error_status = status.HTTP_400_BAD_REQUEST
    if field:
        success['field'] = field

    if message:
        success['message'] = message

    elif code == 200:
        success['status_code'] = 200
        error_status = status.HTTP_200_OK
    elif code == 201:
        success['status_code'] = 201
        error_status = status.HTTP_201_CREATED

    success_response = success_response

    return JsonResponse({'response_details': success_response}, status=error_status)