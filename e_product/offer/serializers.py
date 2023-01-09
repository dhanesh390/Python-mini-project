from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Offer
from e_product_comparison.custom_exception import InvalidValueException


class OfferSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop-product data"""

    def validate(self, data):
        if not isinstance(data['actual_price'], float):
            raise InvalidValueException(f'Invalid price format for actual price{data["actual_price"]}')
        if not isinstance(data['offer_percentage'], float):
            raise InvalidValueException(f'Invalid price format for offer % {data["offer_percentage"]}')
        offer = (data['actual_price'] * data['offer_percentage']) / 100
        price = data['actual_price'] - offer
        data['vendor_price'] = price
        return data

    class Meta:
        model = Offer
        fields = '__all__'


class OfferResponseSerializer(ModelSerializer):
    """ This class is implemented to deserialize the shop product response data"""
    original_price = serializers.FloatField(source='actual_price')
    offer_price = serializers.FloatField(source='vendor_price')

    class Meta:
        model = Offer
        fields = ["id", "original_price", "offer_percentage", "offer_price", "shop", "product"]
