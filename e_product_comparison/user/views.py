import re

import jsonschema
from custom_api_response import custom_error_response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serilalizers import UserResponseSerializer
from .serilalizers import UserSerializer
from .user_constants import USER_SCHEMA, USER, USER_RESPONSE, USER_LIST_RESPONSE, TRUE, FALSE, MESSAGE
from .user_logger import logger


class UserViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the user model instance
    """
    logger.info('Into the user view set')
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        This method overrides the default create method to implement custom functions to the user instance
        :param request: request object of the user instance
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: JsonResponse of the created user object else valid error response
        """
        logger.info('Entering the user creation method')
        try:
            jsonschema.validate(request.data, USER_SCHEMA)
            user = self.get_serializer(data=request.data)
            user.is_valid(raise_exception=TRUE)
            user_instance = user.save()
            user_instance.created_by = user_instance
            user_serializer = self.get_serializer(user_instance, data=request.data)
            user_serializer.is_valid(raise_exception=TRUE)
            user = user_serializer.save()
            user_response = UserResponseSerializer(user)
            logger.info('User successfully created')
            return JsonResponse(user_response.data, status=status.HTTP_201_CREATED)

        except jsonschema.exceptions.ValidationError as ex:
            title = re.findall("'([^']*)'", ex.message)
            logger.error(f'Failed to validate the schema')
            return custom_error_response(title[0], ex.message, 400)

        except ValidationError as ex:
            logger.error(f'{ex} has occurred')
            for title, message in ex.get_full_details().items():
                return custom_error_response(title, message[0].get('message'), 400)

        except ValueError as ex:
            logger.error(f'Value error occurred in user module as {ex.args}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(f'{ex} has occurred')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        This method lists all the users
        :param request: request to get all objects
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the list of all users in Json response object
        """
        try:
            logger.info('Module to list the entire user data')
            users = User.objects.filter(is_active=TRUE)
            if users:
                logger.info('user data retrieved')
                users_serializer = UserResponseSerializer(users, many=TRUE)
                return JsonResponse({'user': users_serializer.data}, status=status.HTTP_200_OK)
            logger.error(USER_LIST_RESPONSE)
            return JsonResponse({USER: USER_LIST_RESPONSE}, status=status.HTTP_200_OK)

        except Exception as ex:
            logger.error(f'{ex} has occurred')
            return custom_error_response(USER, ex.args[0], 400)

    def retrieve(self, request, *args, **kwargs):
        """
        This method is used to get the user by id
        :param request: request to get user associated with the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the user object as json response or return the exception msg as json response
        """
        logger.info('entering the module to retrieve a single user data')
        user_id = kwargs.get('pk')
        try:
            logger.info(f'finding the user object for the {user_id}')
            user = User.objects.filter(is_active=TRUE, id=user_id)
            if user:
                logger.info(f'user object found for the id {user_id} ')
                user_serializer = UserResponseSerializer(user[0])
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            logger.error(f'{USER_RESPONSE} {user_id}')
            return JsonResponse({USER: f'{USER_RESPONSE} {user_id}'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as ex:
            logger.error(f'Invalid value for the key id {user_id}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(USER, ex.args[0], 400)

    def update(self, request, *args, **kwargs):

        """
        This method is used to update the user object
        :param request: To update the user object of the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: returns the updated user object as json response else return the raised exception in json format
        """
        logger.info('entering the module to update an user object')
        try:
            logger.info('Entering the user updating method')
            user = kwargs.get('pk')
            instance = self.get_object()
            instance.updated_by = User.objects.get(is_active=TRUE, id=user)
            if instance.updated_by:
                user_serializer = UserResponseSerializer(instance, data=request.data)
                user_serializer.is_valid(raise_exception=TRUE)
                self.perform_update(user_serializer)
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            logger.error(f'{USER_RESPONSE} {user}')
            return custom_error_response(USER, f'{USER_RESPONSE} {user}', 400)
        except User.DoesNotExist as ex:
            logger.error(f'{USER_RESPONSE} {kwargs.get("pk")}')
            return custom_error_response(USER, ex.args[0], 400)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {kwargs.get("pk")}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)
        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(USER, ex.args[0], 400)


class UserUpdateView(APIView):
    """
     A view set that provides `update()` action for the user model instance
    """
    def delete(self, request):
        """
        This method is used to delete the requested user object
        :param request: data of the user object
        :return: json response of the user object deleted message or else error message
        """
        try:
            logger.info('entering the module to soft delete the user')
            user = User.objects.filter(id=self.request.query_params.get('user-id'))
            if user and user[0].is_active:
                logger.info('user is found to be an active user')
                user[0].is_active = FALSE
                updated_by = User.objects.filter(is_active=True, id=request.headers.get('user'))
                if updated_by:
                    user[0].updated_by = updated_by[0]
                    user[0].save()
                    logger.info('User successfully deleted')
                    return JsonResponse({MESSAGE: 'User successfully deleted'}, status=status.HTTP_200_OK)
                logger.info(f'{USER_RESPONSE} {request.headers.get("user")}')
                return JsonResponse({MESSAGE: f'{USER_RESPONSE} {request.headers.get("user")}'})
            logger.info(f'{USER_RESPONSE}')
            return JsonResponse({MESSAGE: f'{USER_RESPONSE} {self.request.query_params.get("user-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)

        except ValueError as ex:
            logger.error(ex.args[0])
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)
        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(USER, ex.args[0], 400)


class GetUserByRole(APIView):
    """
    This class is implemented to contain method to retrieve the list of users by their role
    """

    def get(self, request):
        """
        This method is used to retrieve the list of users based on their role
        :param request: get list of users based on role
        :return: list of users for the respective role or error response
        """

        try:
            if self.request.query_params.get('role'):
                users = User.objects.filter(is_active=TRUE, user_role=self.request.query_params.get('role'))
            else:
                users = User.objects.filter(is_active=TRUE)
            if users:
                user_serializer = UserResponseSerializer(users, many=TRUE)
                logger.info(f'users successfully returned')
                return JsonResponse({'users': user_serializer.data}, status=status.HTTP_200_OK)
            logger.error(USER_LIST_RESPONSE)
            return JsonResponse({USER: USER_LIST_RESPONSE}, status=status.HTTP_200_OK)
        except ValueError as ex:
            logger.error(f'Invalid value for parameter role {ex.args[0]}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(USER, ex.args[0], 400)

