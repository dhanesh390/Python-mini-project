from rest_framework.serializers import ModelSerializer

from .models import User, Product, ShopDetail, ShopProduct


class UserSerializer(ModelSerializer):
    """ This class is implemented to serialize the user data"""
    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    """ This class is implemented to serialize the product data"""
    class Meta:
        model = Product
        fields = '__all__'


class ShopDetailsSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop details data"""
    class Meta:
        model = ShopDetail
        fields = '__all__'


class ShopProductSerializer(ModelSerializer):
    """ This class is implemented to serialize the shop-product data"""
    class Meta:
        model = ShopProduct
        fields = '__all__'


class ShopProductResponseSerializer(ModelSerializer):
    """ This class is implemented to deserialize the shop product response data"""
    class Meta:
        model = ShopProduct
        fields = ["id", "offer_percentage", "vendor_price", "shop_details", "product", "user"]





































