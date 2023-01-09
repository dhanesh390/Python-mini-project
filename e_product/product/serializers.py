from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Product


class ProductSerializer(ModelSerializer):
    """ This class is implemented to serialize and deserialize the product object"""

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        return data

    # def create(self, validated_data) -> Product:
    #     """
    #     This method is used to create the product object
    #     :param validated_data: valid data of the product instance
    #     :return: created product object
    #     """
    #     return Product.objects.create(**validated_data)


class ProductResponseSerializer(ModelSerializer):
    """
    This class is implemented to deserialize the product response object
    """
    product_name = serializers.CharField(source='name')
    specifications = serializers.JSONField(source='specification')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'category_type', 'specifications']
