from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Offer
from e_product_comparison.custom_exception import InvalidValueException
from .offer_logger import logger
from shop.models import Shop


class OfferSerializer(ModelSerializer):
    logger.info('entering offer serializer module')
    """ This class is implemented to serialize the shop-product data"""

    def validate(self, data):
        if not isinstance(data['actual_price'], float):
            logger.error(f'invalid value for actual price {data["actual_price"]}')
            raise ValueError(f'Invalid price format for actual price{data["actual_price"]}')
        if not isinstance(data['offer_percentage'], float):
            logger.info(f'Invalid price format for offer % {data["offer_percentage"]}')
            raise ValueError(f'Invalid price format for offer % {data["offer_percentage"]}')
        offer = (data['actual_price'] * data['offer_percentage']) / 100
        price = data['actual_price'] - offer
        data['vendor_price'] = price
        logger.info('offer successfully created')
        return data

    class Meta:
        model = Offer
        fields = '__all__'


class OfferResponseSerializer(ModelSerializer):
    logger.info('into the offer deserialized response module')
    """ This class is implemented to deserialize the shop product response data"""
    original_price = serializers.FloatField(source='actual_price')
    offer_price = serializers.FloatField(source='vendor_price')

    class ShopResponseSerializer(ModelSerializer):
        class Meta:
            model = Shop
            fields = ['name']

    shop = ShopResponseSerializer()

    class Meta:
        model = Offer
        fields = ["id", "original_price", "offer_percentage", "offer_price", "product_url", "shop"]
