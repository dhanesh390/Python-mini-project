from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from e_product_comparison.custom_exception import DataNotFoundException
from .models import Product
from .serializers import ProductSerializer, ProductResponseSerializer
from user.models import User
from .product_logger import logger


# Create your views here.
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
        created_by = get_object_or_404(User, id=request.headers.get('user-id'))
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