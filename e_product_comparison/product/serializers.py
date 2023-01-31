from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from .models import Product
from .product_logger import logger


class ProductSerializer(ModelSerializer):
    """ This class is implemented to serialize and deserialize the product object"""
    logger.info('into the product serializer module')

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        if data['name'] is None:
            raise ValidationError('Product name should not be null')

        name = data['name'].upper()
        data['name'] = name
        if data['specification']['color'] is None:
            raise ValidationError('specification color should not be null')
        color = data['specification']['color'].upper()
        data['specification']['color'] = color
        if data['specification']['storage'] is None:
            raise ValidationError('specification storage should not be null')
        storage = data['specification']['storage'].upper()
        data['specification']['storage'] = storage
        return data


class ProductResponseSerializer(ModelSerializer):
    logger.info('into the product deserializer response module')
    """
    This class is implemented to deserialize the product response object
    """

    product_name = serializers.CharField(source='name')
    product_description = serializers.JSONField(source='description')
    category = serializers.CharField(source='category_type')

    class SpecificationSerializer(serializers.JSONField):
        def to_representation(self, value):
            value['product_color'] = value.pop('color')
            value['product_storage'] = value.pop('storage')
            return super().to_representation(value=value)

    product_specifications = SpecificationSerializer(source='specification')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_description', 'category', 'product_specifications']
