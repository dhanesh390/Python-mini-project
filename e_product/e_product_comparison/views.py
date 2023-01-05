from django.contrib.auth.hashers import make_password
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
from .serializers import UserResponseSerializer, ProductResponseSerializer
from .custom_exception import DataNotFoundException, InvalidValue


# Create your views here.
class UserViewSet(ModelViewSet):
    """ This view set class is used to collect and send the user data to the database"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        logger.info('Entering the user creation method')
        password = make_password(request.data['password'], salt=None, hasher='bcrypt')
        request.data['password'] = password
        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        user_instance.created_by = user_instance
        user_serializer = self.get_serializer(user_instance, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            users = get_list_or_404(User, is_active=True)
            if not users:
                raise DataNotFoundException('No user data found ')
        except DataNotFoundException:
            logger.error('No data found for users')
            return JsonResponse({'message': 'No user data found'})
        else:
            users_serializer = UserResponseSerializer(users, many=True)
            return JsonResponse({'user': users_serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # user_id = request.headers.get('id')
        try:
            logger.info(f'finding the user object for the id ')
            user = request.headers

            print('1: ', user)
            print('2: ', user['referer'])
            print('3: ', *args)
            data = self.get_object()
            print('4: ', type(data))
            # data = User.objects.get(id=user.id)
            print('0 :', data)
            #user_instance = get_object_or_404(User, is_active=True, id=user_id)
            if not data:
                raise DataNotFoundException(f'No data found for the id ')
        except DataNotFoundException as ex:
            print(ex)
            logger.error(f'No data found for the user of id, exception occured: {ex}')
            return JsonResponse({'msg': ex}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(f'user object found for the id ')
            user_serializer = UserResponseSerializer(data)
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    # def get_object(self, pk=None):
    #     user_instance = get_object_or_404(User, is_active=True, id=pk)
    #     user = UserResponseSerializer(data=user_instance)
    #     user.is_valid(raise_exception=True)
    #     return JsonResponse(user.data, status=status.HTTP_200_OK)

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

    def list(self, request, *args, **kwargs):
        try:
            products = get_list_or_404(User, is_active=True)
        except DataNotFoundException:
            logger.error('No data found for products')
            raise DataNotFoundException('No product data found ')
        else:
            product_serializer = ProductResponseSerializer(products, many=True)
            return JsonResponse({'product': product_serializer.data}, status=status.HTTP_200_OK)

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
    logger.info('into the shop module')
    queryset = ShopDetail.objects.filter(is_active=True)
    serializer_class = ShopDetailsSerializer

    def create(self, request, *args, **kwargs):
        logger.info('Entering the shop creation module')
        created_by = get_object_or_404(User, id=request.data['user'])
        shop_product_serializer = self.get_serializer(data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        shop_product_serializer.save(created_by=created_by)
        return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.info('entering the shop updation module')
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, id=updated_by)
        shop_detail_serializer = self.get_serializer(instance, data=request.data)
        shop_detail_serializer.is_valid(raise_exception=True)
        self.perform_update(shop_detail_serializer)
        return JsonResponse(shop_detail_serializer.data)


def valid_offer(actual_price, offer_percentage, vendor_price):
    if not vendor_price == (actual_price * offer_percentage) / 100:
        raise InvalidValue('Enter a valid amount')
    return True


class ShopProductViewSet(ModelViewSet):
    """ This view set class is used to collect and send the shop-product data to the database"""
    queryset = ShopProduct.objects.filter(is_active=True)
    serializer_class = ShopProductSerializer

    def create(self, request, *args, **kwargs):
        created_by = get_object_or_404(User, id=request.data['user'])
        actual_price = request.data['actual_price']
        offer = request.data['offer_percentage']
        vendor_price = request.data['vendor_price']
        try:
            if valid_offer(actual_price=actual_price, offer_percentage=offer, vendor_price=vendor_price):
                logger.info('vendor provided a valid price ')
                raise InvalidValue('Invalid price was provided by the vendor')
        except InvalidValue as ex:
            logger.error(f'Invalid vendor price for the offer percentage')
            return JsonResponse({'message': ex}, status=status.HTTP_400_BAD_REQUEST)
        else:
            shop_product_serializer = self.get_serializer(data=request.data)
            shop_product_serializer.is_valid(raise_exception=True)
            shop_product_serializer.save(created_by=created_by)
            return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=False, id=updated_by)
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
        shop_product = get_list_or_404(ShopProduct, id=product_id, is_active=True)
        shop_product_serializer = ShopProductResponseSerializer(shop_product, many=True)
        product = get_object_or_404(Product, id=product_id)
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
        shop_details = get_object_or_404(ShopDetail, id=pk)
        shop_data = {'is_active': False}
        shop_details_serializer = ShopDetailsSerializer(shop_details, data=shop_data, partial=True)
        if shop_details_serializer.is_valid():
            shop_details_serializer.save()
            return JsonResponse(shop_details_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': 'Shop details deletion failed'}, status=status.HTTP_204_NO_CONTENT)
