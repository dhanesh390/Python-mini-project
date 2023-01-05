from django.core.validators import validate_email
from django.utils.functional import empty
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import User, Product, ShopDetail, ShopProduct
import re
from .myconstants import NAME_PATTERN, CONTACT_PATTERN
from .custom_exception import InvalidInput, InvalidValue


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

    # first_name = serializers.CharField(source='first_name')
    # phone = serializers.CharField(source='contact_number')
    class Meta:
        model = User
        fields = '__all__'

    def validate_first_name(self, first_name: str):
        return validate_name(name=first_name)

    def validate_last_name(self, last_name: str):
        return validate_name(name=last_name)

    def validate_contact_number(self, contact_number: str):
        return validate_contact_number(number=contact_number)

    def validate_email(self, email: str) -> str:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email format, Enter again")
        return email

    def create(self, validated_data) -> User:
        return User.objects.create(**validated_data)


class UserResponseSerializer(ModelSerializer):
    phone = serializers.CharField(source='contact_number')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'phone', 'email']


class ProductSerializer(ModelSerializer):
    """ This class is implemented to serialize the product data"""

    # specification = serializers.JSONField(source='specifications')

    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, name: str):
        return validate_name(name=name)

    def create(self, validated_data) -> Product:
        return Product.objects.create(**validated_data)


class ProductResponseSerializer(ModelSerializer):
    # specifications = serializers.JSONField(source='specification')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'specification']


class ShopDetailsSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop details data"""

    class Meta:
        model = ShopDetail
        fields = ['__all__']

    def validate_name(self, name: str):
        return validate_name(name=name)

    def validate_contact_number(self, contact_number: str):
        return validate_contact_number(number=contact_number)

    def create(self, validated_data) -> ShopDetail:
        return ShopDetail.objects.create(**validated_data)


class ShopProductSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop-product data"""
    # actual_price = serializers.FloatField(source='actual_price')
    # offer = serializers.FloatField(source='offer_percentage')
    # vendor_price = serializers.FloatField(source='vendor_price')

    class Meta:
        model = ShopProduct
        fields = '__all__'

    def validate_actual_price(self, actual_price):
        return validate_float_value(actual_price)

    def validate_offer(self, offer_percentage):
        return validate_float_value(offer_percentage)

    def validate_vendor_price(self, vendor_price):
        validate_float_value(vendor_price)

    def create(self, validated_data) -> ShopProduct:
        return ShopProduct.objects.create(**validated_data)


class ShopProductResponseSerializer(ModelSerializer):
    """ This class is implemented to deserialize the shop product response data"""
    original_price = serializers.FloatField(source='actual_price')
    offer_price = serializers.FloatField(source='vendor_price')

    class Meta:
        model = ShopProduct
        fields = ["id", "original_price", "offer_percentage", "offer_price", "shop_detail", "product", "user"]
