from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from e_product_comparison.custom_exception import DataNotFoundException

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serilalizers import UserResponseSerializer
from .serilalizers import UserSerializer
from .user_logger import logger


# Create your views here.
class UserViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the user model instance
    """
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
        try:
            logger.info('Entering the user creation method')
            user = self.get_serializer(data=request.data)
            user.is_valid(raise_exception=True)
            user_instance = user.save()
            user_instance.created_by = user_instance
            user_serializer = self.get_serializer(user_instance, data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            user_response = UserResponseSerializer(user_serializer.data)
            logger.info('User successfully created')
            return JsonResponse(user_response.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print('1: ', e)
            print('2: ', e.args)
            if 'unique constraint' in e.args[0]:
                logger.error('Unique value exception has occured')
                return JsonResponse({'user': {'fields': f'The unique exception occure for the field {e.args[0]}'}})

    def list(self, request, *args, **kwargs):
        """
        This method lists the
        :param request: request to get all objects
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the list of all users in Json response object
        """
        try:
            users = get_list_or_404(User, is_active=True)
            if not users:
                raise DataNotFoundException('No user data found ')
        except DataNotFoundException:
            logger.error('No data found for users')
            return JsonResponse({'message': 'No user data found'})
        else:
            users_serializer = UserResponseSerializer(users, many=True)
            return JsonResponse({'user': users_serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method is used to
        :param request: request to get user associated with the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the user object as json response or return the exception msg as json response
        """
        user_id = kwargs.get('pk')
        try:
            logger.info(f'finding the user object for the id ')
            data = User.objects.get(is_active=True, id=user_id)
            if not data:
                raise DataNotFoundException(f'No data found for the id {user_id}')
        except DataNotFoundException as ex:
            logger.error(f'No data found for the user of id {user_id}')
            return JsonResponse({'msg': ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(f'user object found for the id ')
            user_serializer = UserResponseSerializer(data)
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the user object
        :param request: To update the user object of the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: returns the updated user object as json response else return the raised exception in json format
        """
        logger.info('Entering the user updating method')
        updated_by = kwargs.get('pk')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, id=updated_by)
        user_serializer = UserResponseSerializer(instance, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    """
     A view set that provides `update()` action for the user model instance
    """

    @staticmethod
    def patch(request, pk=None):
        """
        This method is used to delete the requested user object
        :param request: data of the user object
        :param pk: id of the user object to be deleted
        :return: json response of the user object deleted message or else error message
        """
        user = User.objects.get(pk=pk)
        user_data = {'is_active': False}
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'msg': 'User successfully deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class GetUserByRole(APIView):

    @staticmethod
    def get(request, user_role=None):
        users = get_list_or_404(User, user_role=user_role, is_active=True)
        user_serializer = UserResponseSerializer(users, many=True)
        return JsonResponse({'users': user_serializer.data}, status=status.HTTP_200_OK)

