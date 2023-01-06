from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .e_product_logger import logger

from .models import User, Shop, Product, Offer
from .serializers import UserSerializer, ShopDetailsSerializer, ProductSerializer, OfferSerializer
from .serializers import UserResponseSerializer, ProductResponseSerializer, OfferResponseSerializer
from .custom_exception import DataNotFoundException


# Create your views here.
class UserViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the user model instance
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        This method overrides the default create method to implement custom functions to the user instance
        :param request: request object of the user instance
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: JsonResponse of the created user object else valid error response
        """
        logger.info('Entering the user creation method')
        password = make_password(request.data['password'], salt=None, hasher='bcrypt')
        request.data['password'] = password
        print('1: ', request.data)
        print('1.1: ', request.data['contact_number'])
        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        user_instance.created_by = user_instance
        user_serializer = self.get_serializer(user_instance, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        user_response = UserResponseSerializer(user_serializer.data)
        return JsonResponse(user_response.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        This method lists the
        :param request: request to get all objects
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the list of all users in Json response object
        """
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
        """
        This method is used to
        :param request: request to get user associated with the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: Returns the user object as json response or return the exception msg as json response
        """
        user_id = kwargs.get('pk')
        try:
            logger.info(f'finding the user object for the id ')
            data = User.objects.get(is_active=True, id=user_id)
            if not data:
                raise DataNotFoundException(f'No data found for the id {user_id}')
        except DataNotFoundException as ex:
            logger.error(f'No data found for the user of id {user_id}')
            return JsonResponse({'msg': ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(f'user object found for the id ')
            user_serializer = UserResponseSerializer(data)
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the user object
        :param request: To update the user object of the request id
        :param args: extra positional argument for user object
        :param kwargs: extra keyword argument for user object
        :return: returns the updated user object as json response else return the raised exception in json format
        """
        logger.info('Entering the user updating method')
        updated_by = kwargs.get('pk')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, id=updated_by)
        user_serializer = UserResponseSerializer(instance, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the product model instance
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the product objects from the request instance
        :param request: product instance to create a new product object
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return:
        """
        created_by = get_object_or_404(User, id=request.data['user'])
        product_serializer = self.get_serializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save(created_by=created_by)
        return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        This method lists all the products
        :param request: To return the list of product objects
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return: list of product objects in json response or else DatoNotFound exception is returned
        """
        try:
            products = get_list_or_404(Product, is_active=True)
        except DataNotFoundException:
            logger.error('No data found for products')
            raise DataNotFoundException('No product data found ')
        else:
            product_serializer = ProductResponseSerializer(products, many=True)
            return JsonResponse({'product': product_serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the instance of the product object
        :param request: id of the requested product object
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return: product details in Json response or raise exception in Json format
        """
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(Product, is_active=True, id=updated_by)
        product_serializer = self.get_serializer(instance, data=request.data)
        product_serializer.is_valid(raise_exception=True)
        self.perform_update(product_serializer)
        return JsonResponse(product_serializer.data)


class ShopDetailsViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the shop model instance
    """
    logger.info('into the shop module')
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopDetailsSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the shop object from the request
        :param request: data object for the shop instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the json response of the shop object or error response of the same
        """
        logger.info('Entering the shop creation module')
        created_by = get_object_or_404(User, id=request.data['user'])
        shop_product_serializer = self.get_serializer(data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        shop_product_serializer.save(created_by=created_by)
        return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the shop object
        :param request: data to update the shop object of the instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the updated shop object as json response or error message in the same format
        """
        logger.info('entering the shop updating module')
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, id=updated_by)
        shop_detail_serializer = self.get_serializer(instance, data=request.data)
        shop_detail_serializer.is_valid(raise_exception=True)
        self.perform_update(shop_detail_serializer)
        return JsonResponse(shop_detail_serializer.data)


def calculate_vendor_price(actual_price, offer_percentage):
    offer_price = (actual_price * offer_percentage) / 100
    return actual_price - offer_price


class ShopProductViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
     'list()` actions for the shop_product model instance
    """
    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the shop_product object for the instance
        :param request: data to create new shop_product instance
        :param args: extra positional argument for shop_product object
        :param kwargs: extra keyword argument for shop_product object
        :return: returns the json response of the created object or error response in the same format
        """
        created_by = get_object_or_404(User, id=request.data['user'])
        actual_price = request.data['actual_price']
        offer = request.data['offer_percentage']
        vendor_price = calculate_vendor_price(actual_price=actual_price, offer_percentage=offer)
        request.data['vendor_price'] = vendor_price
        shop_product_serializer = self.get_serializer(data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        shop_product_serializer.save(created_by=created_by)
        return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the shop_product instance object
        :param request: id of the shop_product object to be updated
        :param args: extra positional argument for shop_product object
        :param kwargs: extra keyword argument for shop_product object
        :return: returns the json response of the updated shop_product object or error response in the same
        """
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=False, id=updated_by)
        shop_product_serializer = self.get_serializer(instance, data=request.data)
        shop_product_serializer.is_valid(raise_exception=True)
        self.perform_update(shop_product_serializer)
        return JsonResponse(shop_product_serializer.data)


class UserUpdateView(APIView):
    """
     A view set that provides `update()` action for the user model instance
    """

    @staticmethod
    def patch(request, pk=None):
        """
        This method is used to delete the requested user object
        :param request: data of the user object
        :param pk: id of the user object to be deleted
        :return: json response of the user object deleted message or else error message
        """
        user = User.objects.get(pk=pk)
        user_data = {'is_active': False}
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'msg': 'User successfully deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateViewSet(APIView):
    """
     A view set that provides `update()` action for the product model instance
    """

    @staticmethod
    def patch(request, product_id=None):
        """
        This method is used to delete the product object of the instance
        :param request: data of the product object
        :param product_id: id of the required product
        :return: json response of the successful deletion message or error response message
        """
        product = get_object_or_404(Product, product_id=product_id)
        product_data = {'is_active': False}
        product_serializer = ProductSerializer(product, data=product_data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse({'msg': 'User successfully deleted'}, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class ShopProductUpdateViewSet(APIView):
    """
     A view set that provides `update()` action for the offer model instance
    """

    @staticmethod
    def patch(request, offer_id=None):
        """
        This method is used to delete the offer instance
        :param request: Data's of the offer instance
        :param offer_id: id of the offer object
        :return: returns the updated response message
        """
        shop_product = get_object_or_404(Offer, offer_id=offer_id)
        shop_product_data = {'is_active': False}
        shop_product_serializer = OfferSerializer(shop_product, data=shop_product_data, partial=True)
        if shop_product_serializer.is_valid():
            shop_product_serializer.save()
            return JsonResponse({'message': 'offer successfully updated '}.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)


class offerView(APIView):
    """
     A view set that provides `get()` action for the offer model instance
    """

    @staticmethod
    def get(request, product_id=None):
        shop_product = get_list_or_404(Offer, product_id=product_id, is_active=True)
        shop_product_serializer = OfferResponseSerializer(shop_product, many=True)
        product = get_object_or_404(Product, id=product_id)
        product_serializer = ProductResponseSerializer(product)
        response = {'product': product_serializer.data, 'shop_product': shop_product_serializer.data}
        return JsonResponse(response, status=status.HTTP_200_OK)


class ViewOffersByProductName(APIView):
    """
         A view set that provides `get()` action for the offer model instance
        """
    @staticmethod
    def get(request, name=None):
        product = get_object_or_404(Offer, name=name, is_active=True)
        print('1: product')
        product_serializer = ProductResponseSerializer(product)
        offers = get_list_or_404(Offer, product_id=product.id, is_active=True)
        offer_serializer = OfferResponseSerializer(offers, many=True)
        response = {'product': product_serializer.data, 'offers': offer_serializer.data}
        return JsonResponse(response, status=status.HTTP_200_OK)


class ShopDetailsUpdateView(APIView):
    """
     A view set that provides `update()` action for the shop model instance
    """

    @staticmethod
    def patch(request, pk=None):
        shop_details = get_object_or_404(Shop, id=pk)
        shop_data = {'is_active': False}
        shop_details_serializer = ShopDetailsSerializer(shop_details, data=shop_data, partial=True)
        if shop_details_serializer.is_valid():
            shop_details_serializer.save()
            return JsonResponse(shop_details_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': 'Shop details deletion failed'}, status=status.HTTP_204_NO_CONTENT)
