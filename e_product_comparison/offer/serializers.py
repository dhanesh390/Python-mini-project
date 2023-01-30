from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from shop.models import Shop

from .models import Offer
from .offer_logger import logger


class OfferSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop-product data"""
    logger.info('entering offer serializer module')

    # actual_price = serializers.FloatField(source='original_price')
    # offer_percentage = serializers.FloatField(source='discount')
    # vendor_price = serializers.FloatField(source='discount_price')

    # class Meta:
    #     model = Offer
    #     fields = ['product', 'shop', 'actual_price', 'offer_percentage', 'vendor_price']

    class Meta:
        model = Offer
        fields = '__all__'

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


class OfferResponseSerializer(ModelSerializer):
    """ This class is implemented to deserialize the shop product response data"""
    logger.info('into the offer deserialized response module')

    original_price = serializers.FloatField(source='actual_price')
    discount = serializers.FloatField(source='offer_percentage')
    discount_price = serializers.FloatField(source='vendor_price')

    class ShopResponseSerializer(ModelSerializer):
        class Meta:
            model = Shop
            fields = ['name']

    shop = ShopResponseSerializer()

    class Meta:
        model = Offer
        fields = ["id", "original_price", "discount", "discount_price", "product_url", "shop"]

