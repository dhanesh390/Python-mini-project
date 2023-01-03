from rest_framework.serializers import ModelSerializer
from .models import User, Product, ShopDetails, ShopProduct


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class CategorySerializer(ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopDetailsSerializer(ModelSerializer):
    class Meta:
        model = ShopDetails
        fields = '__all__'


class ShopProductSerializer(ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = '__all__'


class ShopProductResponseSerializer(ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ["shop_product_id", "offer_percentage", "vendor_price", "shop_details", "product", "user"]





































