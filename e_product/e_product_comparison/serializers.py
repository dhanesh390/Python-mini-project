from django.core.validators import validate_email
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, status
from rest_framework.serializers import ValidationError

from .models import User, Product, Shop, Offer
import re
from .myconstants import NAME_PATTERN, CONTACT_PATTERN
from .custom_exception import InvalidInput, AlreadyExistException
from .e_product_logger import logger


def validate_name(name: str):
    if not re.match(NAME_PATTERN, name):
        raise ValidationError('Invalid name, Enter a valid name')
    return name


def validate_contact_number(number: str):
    if not re.match(CONTACT_PATTERN, number):
        raise ValidationError('Invalid phone number, Enter a valid phone number')
    return number


def validate_float_value(value):
    if not isinstance(value, float):
        raise InvalidInput('Enter the valid float value')
    return value


class UserSerializer(ModelSerializer):
    """ This class is implemented to serialize the user data"""
    print('2: ')

    class Meta:
        model = User
        fields = '__all__'

    print('3')

    def validate_first_name(self, first_name: str):
        print('4')
        """
        This method is used to validate the first name of the user object
        :param first_name: first name of user instance
        :return: validated first name  or error response
        """
        return validate_name(name=first_name)

    def validate_last_name(self, last_name: str):
        print('5')
        """
        This method is used to validate the last name of the user object
        :param last_name: last name of user instance
        :return: validated last name or error response
        """
        return validate_name(name=last_name)

    def validate_user_name(self, username: str):
        print('6')
        """
        This method is used to validate whether the username is already exist or not
        :param username: username of the user instance object
        :return: validated username or error response
        """
        users = User.objects.all()
        for user in users:
            if user.username == username:
                raise AlreadyExistException(detail=f'This username {username} already exists',
                                            code=status.HTTP_208_ALREADY_REPORTED)
            else:
                return username

    def validate_contact_number(self, contact_number: str):
        print('7')
        """
        This method is used to validate the contact number of the user object
        :param contact_number: contact number of user instance
        :return: validated contact number or error response
        """
        users = User.objects.all()
        for user in users:
            print('8: ', contact_number)
            if user.contact_number == contact_number:
                raise AlreadyExistException(detail=f'This contact {contact_number} already exists',
                                            code=status.HTTP_208_ALREADY_REPORTED)
            else:
                return validate_contact_number(contact_number)

    def validate_email(self, email: str) -> str:
        """
        This method is used to validate the email of the user object
        :param email: email data of the user instance
        :return: validated user email or error response
        """
        users = User.objects.all()
        for user in users:
            print('1.1: ', user.email)
            print('2.1: ', email)
            if user.email == email:
                print('3.1')
                raise AlreadyExistException(detail=f'This email {email} already exists',
                                            code=status.HTTP_208_ALREADY_REPORTED)
            else:
                try:
                    validate_email(email)
                except AlreadyExistException:
                    logger.error(f'This email {email} already exists')
                except ValidationError:
                    raise ValidationError("Invalid email format, Enter again")
                return email

    def create(self, validated_data) -> User:
        """
        This method is used to create the user instance using the validated data
        :param validated_data: valid data of the user instance
        :return: user object
        """
        return User.objects.create(**validated_data)


class UserResponseSerializer(ModelSerializer):
    """
    This class is implemented to deserialize the user response object
    """

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'is_active', 'is_seller']


class ProductResponseSerializer(ModelSerializer):
    """
    This class is implemented to deserialize the product response object
    """
    product_name = serializers.CharField(source='name')
    specifications = serializers.JSONField(source='specification')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'category_type', 'specifications']


class ProductSerializer(ModelSerializer):
    """ This class is implemented to serialize and deserialize the product object"""

    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, name: str):
        """
        This method is used to validate the name of the product instance
        :param name: name of the product
        :return: validated name or error response
        """
        return validate_name(name=name)

    def create(self, validated_data) -> Product:
        """
        This method is used to create the product object
        :param validated_data: valid data of the product instance
        :return: created product object
        """
        return Product.objects.create(**validated_data)


class ShopDetailsSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop details data"""

    class Meta:
        model = Shop
        fields = '__all__'

    def validate_name(self, name: str):
        """
        This method is used to validate the name of the shop object
        :param name: shop name of the shop instance
        :return: validated name or error response
        """
        return validate_name(name=name)

    def validate_contact_number(self, contact_number: str):
        """
        This method is used to validate the contact number of the shop instance
        :param contact_number: shop data containing contact number
        :return: validated contact number or error response
        """
        return validate_contact_number(number=contact_number)

    def create(self, validated_data) -> Shop:
        """
        This method is used to create the shop object with validated data
        :param validated_data: valid data of the shop object
        :return: created shop object
        """
        return Shop.objects.create(**validated_data)


class OfferSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop-product data"""

    class Meta:
        model = Offer
        fields = '__all__'

    def validate_actual_price(self, actual_price):
        """
        This method is used to validate the actual price details
        :param actual_price: original price of the product
        :return: Validated actual price
        """
        return validate_float_value(actual_price)

    def validate_offer(self, offer_percentage):
        """
        This method is used to validate the offer percentage details
        :param offer_percentage: offer data of the product
        :return: validated offer percentage
        """
        return validate_float_value(offer_percentage)

    def validate_vendor_price(self, vendor_price):
        """
        This method is used to validate the vendor price
        :param vendor_price: offer price provided by the vendor
        :return: validated vendor price
        """
        return validate_float_value(vendor_price)

    def create(self, validated_data) -> Offer:
        """
        This method is used to create the shop_product object using the validated data
        :param validated_data: valid data's of the shop_product instance
        :return: shop_product object
        """
        return Offer.objects.create(**validated_data)


class OfferResponseSerializer(ModelSerializer):
    """ This class is implemented to deserialize the shop product response data"""
    original_price = serializers.FloatField(source='actual_price')
    offer_price = serializers.FloatField(source='vendor_price')

    class Meta:
        model = Offer
        fields = ["id", "original_price", "offer_percentage", "offer_price", "shop", "product", "user"]
