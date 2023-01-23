import re

import jsonschema
from jsonschema import Validator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.templatetags.rest_framework import data
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError

from .models import User
from .serilalizers import UserResponseSerializer
from .serilalizers import UserSerializer
from .user_logger import logger
from e_product_comparison.custom_exception import DataNotFoundException
from e_product_comparison.myconstants import MESSAGE, TRUE, FALSE, USER_SCHEMA, USER_RESPONSE, USER, USER_LIST_RESPONSE

from custom_api_response import api_exception_handler
from custom_api_response import custom_error_response


class UserViewSet(ModelViewSet):
    logger.info('Into the user view set')
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the user model instance
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        logger.info('Entering the user creation method')
        """
        This method overrides the default create method to implement custom functions to the user instance
        :param request: request object of the user instance
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: JsonResponse of the created user object else valid error response
        """
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
            logger.info('user data retrieved')
            if users:
                users_serializer = UserResponseSerializer(users, many=TRUE)
                return JsonResponse({'user': users_serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.error(USER_LIST_RESPONSE)
                return custom_error_response(USER, USER_LIST_RESPONSE, 400)

        except Exception as ex:
            logger.error('No data found for the users')
            return custom_error_response(USER, ex.args[0], 400)

    def retrieve(self, request, *args, **kwargs):
        logger.info('entering the module to retrieve a single user data')
        """
        This method is used to get the user by id
        :param request: request to get user associated with the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the user object as json response or return the exception msg as json response
        """
        user_id = kwargs.get('pk')
        try:
            logger.info(f'finding the user object for the id ')
            user = User.objects.get(is_active=TRUE, id=user_id)
            logger.info(f'user object found for the id ')
            user_serializer = UserResponseSerializer(user)
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f'{USER_RESPONSE} of id {user_id}')
            return custom_error_response(USER,  f'{USER_RESPONSE} {user_id}', 400)

        except ValueError as ex:
            logger.error(f'Invalid value for the key id {user_id}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

    def update(self, request, *args, **kwargs):
        logger.info('entering the module to update an user object')
        """
        This method is used to update the user object
        :param request: To update the user object of the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: returns the updated user object as json response else return the raised exception in json format
        """
        try:
            logger.info('Entering the user updating method')
            updated_by = kwargs.get('pk')
            instance = self.get_object()
            instance.updated_by = User.objects.get(is_active=TRUE, id=updated_by)
            if instance.updated_by:
                user_serializer = UserResponseSerializer(instance, data=request.data)
                user_serializer.is_valid(raise_exception=TRUE)
                self.perform_update(user_serializer)
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(f'{USER_RESPONSE} {updated_by}')
                return custom_error_response(USER, f'{USER_RESPONSE} {updated_by}', 400)
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

    @staticmethod
    def delete(request, pk=None):
        logger.info('entering the module to soft delete the user')
        """
        This method is used to delete the requested user object
        :param request: data of the user object
        :param pk: id of the user object to be deleted
        :return: json response of the user object deleted message or else error message
        """
        try:
            user = User.objects.get(pk=pk)
            if user.is_active:
                user.is_active = FALSE
                user.save()
                return JsonResponse({MESSAGE: 'User successfully deleted'}, status=status.HTTP_200_OK)
            return JsonResponse({MESSAGE: f'{USER_RESPONSE} {pk}'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f'{USER_RESPONSE} {pk}')
            return custom_error_response(USER, f'{USER_RESPONSE} {pk}', 400)
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

    @staticmethod
    def get(request, role=None):
        """
        This method is used to retrieve the list of users based on their role
        :param request: get list of users based on role
        :param role: name of the role
        :return: list of users for the respective role or error response
        """
        try:
            users = User.objects.filter(user_role=role, is_active=TRUE)
            if users:
                user_serializer = UserResponseSerializer(users, many=TRUE)
                logger.info(f'users for the role {role} successfully returned')
                return JsonResponse({'users': user_serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.error(USER_LIST_RESPONSE)
                return custom_error_response(USER, USER_LIST_RESPONSE, 400)
        except ValueError as ex:
            logger.error(f'Invalid value for parameter role {ex.args[0]}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(USER, ex.args[0], 400)
