import re

from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from .models import User
from .user_constants import NAME_PATTERN, CONTACT_PATTERN
from .user_logger import logger


class UserSerializer(ModelSerializer):
    """ This class is implemented to serialize the user data"""

    def validate(self, data):
        """
        This method is used to validate the data of the user object
        :param data: user instance data object
        :return: validated data of the user object
        """
        logger.info('Entering the user serializer validation ')
        if not re.match(NAME_PATTERN, data['first_name']):
            logger.error(f'Invalid first name {data["first_name"]}')
            raise ValidationError(f'Invalid first name {data["first_name"]}, Enter a valid name')
        if not re.match(NAME_PATTERN, data['last_name']):
            logger.error(f'Invalid last name {data["last_name"]}')
            raise ValidationError(f'Invalid last name {data["last_name"]}, Enter a valid name')
        if len(data['username']) < 6:
            raise ValidationError('username should be more than 6 characters')
        if len(data['contact_number']) != 10 and not re.match(CONTACT_PATTERN, data['contact_number']):
            logger.error(f'Invalid contact number {data["contact_number"]}')
            raise ValidationError(f'Invalid contact number {data["contact_number"]}, Enter a valid contact number')

        try:
            validate_email(data['email'])
            logger.info('user email is valid')
        except ValidationError:
            logger.error('Invalid email value')
            raise ValidationError(f'Invalid email {data["email"]}, Enter again')
        if data['password']:
            logger.info('decrypting the password')
            password = make_password(data['password'], salt=None, hasher='bcrypt')
            data['password'] = password
        logger.info('user data successfully validated and serialized')
        return data

    class Meta:
        model = User
        fields = '__all__'


class UserResponseSerializer(ModelSerializer):
    logger.info('Entering the user deserialized response module')
    """
    This class is implemented to deserialize the user response object
    """

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'is_active', 'is_seller']
