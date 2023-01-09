from rest_framework.serializers import ModelSerializer

from .models import Shop


class ShopDetailsSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop details data"""

    class Meta:
        model = Shop
        fields = '__all__'

    # def create(self, validated_data) -> Shop:
    #     """
    #     This method is used to create the shop object with validated data
    #     :param validated_data: valid data of the shop object
    #     :return: created shop object
    #     """
    #     return Shop.objects.create(**validated_data)
