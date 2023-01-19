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
from e_product_comparison.myconstants import TRUE, FALSE, MESSAGE


# Create your views here.
class ProductViewSet(ModelViewSet):
    logger.info('entering the product view set module')
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the product model instance
    """
    queryset = Product.objects.filter(is_active=TRUE)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        logger.info('into the product creation module')
        """
        This method is used to create the product objects from the request instance
        :param request: product instance to create a new product object
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return:
        """
        try:
            created_by = get_object_or_404(User, id=request.headers.get('user-id'))
            product_serializer = self.get_serializer(data=request.data)
            product_serializer.is_valid(raise_exception=TRUE)
            product_serializer.save(created_by=created_by)
            logger.info('product successfully created')
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            logger.error(f'No data found for the user of id {request.headers.get("user-id")}')
            return JsonResponse({MESSAGE: f'No data found for the user of id {request.headers.get("user-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the user id {request.headers.get("user-id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        logger.info('into the module to retrieve the list of products')
        """
        This method lists all the products
        :param request: To return the list of product objects
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return: list of product objects in json response or else DatoNotFound exception is returned
        """
        try:
            products = get_list_or_404(Product, is_active=TRUE)
            logger.info('list of products successfully retrieved')
        except Product.DoesNotExist:
            logger.error('No data found for products')
            return JsonResponse({MESSAGE: 'No data found for products'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            product_serializer = ProductResponseSerializer(products, many=TRUE)
            return JsonResponse({'product': product_serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        logger.info('into the product updating module')
        """
        This method is used to update the instance of the product object
        :param request: id of the requested product object
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return: product details in Json response or raise exception in Json format
        """
        try:
            updated_by = request.headers.get("id")
            instance = self.get_object()
            instance.updated_by = get_object_or_404(Product, is_active=TRUE, id=updated_by)
            product_serializer = self.get_serializer(instance, data=request.data)
            product_serializer.is_valid(raise_exception=TRUE)
            self.perform_update(product_serializer)
            return JsonResponse(product_serializer.data)
        except Product.DoesNotExist:
            logger.error('No data found for products')
            return JsonResponse({MESSAGE: 'No data found for products'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {request.headers.get("id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateViewSet(APIView):
    """
     A view set that provides `update()` action for the product model instance
    """

    @staticmethod
    def patch(request, product_id=None):
        logger.info('entering the module to soft delete the data')
        """
        This method is used to delete the product object of the instance
        :param request: data of the product object
        :param product_id: id of the required product
        :return: json response of the successful deletion message or error response message
        """
        try:
            product = get_object_or_404(Product, id=product_id)
            product_data = {'is_active': FALSE}
            product_serializer = ProductSerializer(product, data=product_data, partial=TRUE)
            if product_serializer.is_valid():
                product_serializer.save()
                return JsonResponse({MESSAGE: 'product successfully deleted'}, status=status.HTTP_200_OK)
            return JsonResponse({MESSAGE: "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            logger.error(f'No data found for the product of id {product_id}')
            return JsonResponse({MESSAGE: f'No data found for the product of id {product_id}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key product id {product_id}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
