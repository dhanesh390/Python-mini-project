from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .e_product_logger import logger


from .models import User, ShopDetail, Product, ShopProduct
from .serializers import ShopProductSerializer
from .serializers import UserSerializer, ShopDetailsSerializer, ProductSerializer, ShopProductResponseSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    """ This view set class is used to collect and send the user data to the database"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        logger.info('Entering the user creation method')
        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        user_instance.created_by = user_instance
        user_serializer = self.get_serializer(user_instance, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        logger.info('Entering the user updation method')
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, user_id=updated_by)
        user_serializer = self.get_serializer(instance, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(ModelViewSet):
    """ This view set class is used to collect and send the product data to the database"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        created_by = get_object_or_404(User, id=request.data['user'])
        product_serializer = self.get_serializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save(created_by=created_by)
        return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(Product, is_active=True, id=updated_by)
        product_serializer = self.get_serializer(instance, data=request.data)
        product_serializer.is_valid(raise_exception=True)
        self.perform_update(product_serializer)
        return JsonResponse(product_serializer.data)


class ShopDetailsViewSet(ModelViewSet):
    """ This view set class is used to collect and send the shop details data to the database"""
    queryset = ShopDetail.objects.filter(is_active=True)
    serializer_class = ShopDetailsSerializer

    def create(self, request, *args, **kwargs):
        created_by = get_object_or_404(User, user_id=request.data['user'])
        shop_product_serializer = self.get_serializer(data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        shop_product_serializer.save(created_by=created_by)
        return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, user_id=updated_by)
        shop_detail_serializer = self.get_serializer(instance, data=request.data)
        shop_detail_serializer.is_valid(raise_exception=True)
        self.perform_update(shop_detail_serializer)
        return JsonResponse(shop_detail_serializer.data)


class ShopProductViewSet(ModelViewSet):
    """ This view set class is used to collect and send the shop-product data to the database"""
    queryset = ShopProduct.objects.filter(is_active=True)
    serializer_class = ShopProductSerializer

    def create(self, request, *args, **kwargs):
        created_by = get_object_or_404(User, user_id=request.data['user'])
        shop_product_serializer = self.get_serializer(data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        shop_product_serializer.save(created_by=created_by)
        return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=False, user_id=updated_by)
        shop_product_serializer = self.get_serializer(instance, data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        self.perform_update(shop_product_serializer)
        return JsonResponse(shop_product_serializer.data)


class UserUpdateView(APIView):
    """ This view set class is used to collect and send the updated user data to the database"""

    @staticmethod
    def patch(request, pk=None):
        user = User.objects.get(pk=pk)
        user_data = {'is_active': False}
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateViewSet(APIView):
    """ This view set class is used to collect and send the updated product data to the database"""

    @staticmethod
    def patch(request, product_id=None):
        product = get_object_or_404(Product, product_id=product_id)
        product_data = {'is_active': False}
        product_serializer = ProductSerializer(product, data=product_data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ShopProductUpdateViewSet(APIView):
    """ This view set class is used to collect and send the updated shop product data to the database"""

    @staticmethod
    def patch(request, shop_product_id=None):
        shop_product = get_object_or_404(ShopProduct, shop_product_id=shop_product_id)
        shop_product_data = {'is_active': False}
        shop_product_serializer = ShopProductSerializer(shop_product, data=shop_product_data, partial=True)
        if shop_product_serializer.is_valid():
            shop_product_serializer.save()
            return JsonResponse(shop_product_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ShopProductView(APIView):
    """ This view set class is used to collect and send the shop product data from the database"""

    @staticmethod
    def get(request, product_id=None):
        shop_product = get_list_or_404(ShopProduct, product_id=product_id, is_active=True)
        shop_product_serializer = ShopProductResponseSerializer(shop_product, many=True)
        product = get_object_or_404(Product, product_id=product_id)
        product_serializer = ProductSerializer(product)
        response = {'product': product_serializer.data, 'shop_product': shop_product_serializer.data}
        return JsonResponse(response, status=status.HTTP_200_OK)


class ShopDetailsUpdateView(APIView):
    """
     This view set class is used to collect and send the shop details data to the database using API view set and
     as well as return those data's when asked
    """

    @staticmethod
    def patch(request, pk=None):
        shop_details = get_object_or_404(ShopDetail, shop_id=pk)
        shop_data = {'is_active': False}
        shop_details_serializer = ShopDetailsSerializer(shop_details, data=shop_data, partial=True)
        if shop_details_serializer.is_valid():
            shop_details_serializer.save()
            return JsonResponse(shop_details_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': 'Shop details deletion failed'}, status=status.HTTP_204_NO_CONTENT)




