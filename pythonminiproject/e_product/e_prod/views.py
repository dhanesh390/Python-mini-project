from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from .serializers import UserSerializer, ShopDetailsSerializer, ProductSerializer, CategorySerializer
from .serializers import ShopProductSerializer
from .models import User, ShopDetails, Product, Category, ShopProduct


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


# class ShopDetailsViewSet(ModelViewSet):
#     queryset = ShopDetails.objects.filter(is_active=True)
#     serializer_class = ShopDetailsSerializer


class ShopProductViewSet(ModelViewSet):
    queryset = ShopProduct.objects.filter(is_active=True)
    serializer_class = ShopProductSerializer


class UserUpdateView(APIView):

    @staticmethod
    def patch(request, pk=None):
        user = User.objects.get(pk=pk)
        user_data = {'is_active': False}
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ShopDetailsCrud(APIView):

    @staticmethod
    def post(request):
        shop_details_serializers = ShopDetailsSerializer(data=request.data)
        shop_details_serializers.is_valid(raise_exception=True)
        shop_details_serializers.save()
        return JsonResponse(shop_details_serializers.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request, pk=None):
        if pk:
            shop_details = get_object_or_404(ShopDetails, id=pk)
            shop_details_serializers = ShopDetailsSerializer(shop_details)
            return JsonResponse(shop_details_serializers.data, status=status.HTTP_200_OK)
        else:
            shop_details = ShopDetails.objects.all()
            shop_details_serializers = ShopDetailsSerializer(shop_details, many=True)
            return JsonResponse(shop_details_serializers.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk=None):
        shop_details = get_object_or_404(ShopDetails, id=pk)
        shop_details_serializers = ShopDetailsSerializer(instance=shop_details, data=request.data)
        shop_details_serializers.is_valid(raise_exception=True)
        shop_details_serializers.save()
        return JsonResponse(shop_details_serializers.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, pk=None):
        shop_details = ShopDetails.objects.get(pk=pk)
        print(shop_details)
        shop_data = {'is_active': False}
        shop_details_serializer = ShopDetailsSerializer(shop_details, data=shop_data, partial=True)
        if shop_details_serializer.is_valid():
            shop_details_serializer.save()
            return JsonResponse(shop_details_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': 'Shop details deletion failed'}, status=status.HTTP_204_NO_CONTENT)











