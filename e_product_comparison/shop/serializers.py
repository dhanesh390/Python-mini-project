from rest_framework.serializers import ModelSerializer
from user.models import User

from .models import Shop
from .shop_logger import logger


class ShopDetailsSerializer(ModelSerializer):
    logger.info('entering the shop serializer module')
    """ This class is implemented to serialize the shop details data"""

    class Meta:
        model = Shop
        fields = '__all__'


class ShopResponseSerializer(ModelSerializer):
    logger.info('entering the shop deserialized response module')
    """
     This serializer class is implemented to customize the response shop response
    """

    class UserResponseSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']

    user = UserResponseSerializer()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'contact_number', 'building_no', 'street_name', 'locality', 'district', 'state',
                  'country', 'pincode', 'is_active', 'user']
