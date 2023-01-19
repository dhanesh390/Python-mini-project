from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Product
from .product_logger import logger


class ProductSerializer(ModelSerializer):
    logger.info('into the product serializer module')
    """ This class is implemented to serialize and deserialize the product object"""

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        return data


class ProductResponseSerializer(ModelSerializer):
    logger.info('into the product deserializer response module')
    """
    This class is implemented to deserialize the product response object
    """
    product_name = serializers.CharField(source='name')
    specifications = serializers.JSONField(source='specification')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'category_type', 'specifications']
