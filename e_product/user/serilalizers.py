import re

from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from e_product_comparison.myconstants import CONTACT_PATTERN, NAME_PATTERN
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from .models import User
from .user_logger import logger


def is_valid_name(name: str):
    if not re.match(NAME_PATTERN, name):
        return False
    return True


def is_valid_contact_number(number: str):
    if not re.match(CONTACT_PATTERN, number):
        return False
    return True


class UserSerializer(ModelSerializer):
    """ This class is implemented to serialize the user data"""

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        """
        This method is used to validate the data of the user object
        :param data: user instance data object
        :return: validated data of the user object
        """
        if not re.match(NAME_PATTERN, data['first_name']):
            logger.error(f'Invalid first name {data["first_name"]}')
            raise ValidationError(f'Invalid first name {data["first_name"]}, Enter a valid name')
        if not re.match(NAME_PATTERN, data['last_name']):
            logger.error(f'Invalid last name {data["last_name"]}')
            raise ValidationError(f'Invalid last name {data["last_name"]}, Enter a valid name')
        if len(data['username']) < 6:
            raise ValidationError('username should be more than 6 characters')
        if not re.match(CONTACT_PATTERN, data['contact_number']):
            logger.error(f'Invalid contact number {data["contact_number"]}')
            raise ValidationError(f'Invalid contact number {data["contact_number"]}, Enter a valid contact number')

        try:
            validate_email(data['email'])
        except ValidationError:
            logger.error('Invalid email value')
            raise ValidationError(f'Invalid email {data["email"]}, Enter again' )
        if data['password']:
            logger.info('decrypting the password')
            password = make_password(data['password'], salt=None, hasher='bcrypt')
            data['password'] = password
        return data


class UserResponseSerializer(ModelSerializer):
    """
    This class is implemented to deserialize the user response object
    """

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'is_active', 'is_seller']