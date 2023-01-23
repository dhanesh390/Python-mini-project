import re

import jsonschema
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from e_product_comparison.custom_exception import DataNotFoundException
from .models import Product
from .serializers import ProductSerializer, ProductResponseSerializer
from user.models import User
from .product_logger import logger
from e_product_comparison.myconstants import TRUE, FALSE, MESSAGE, PRODUCT_SCHEMA, PRODUCT, PRODUCT_LIST_RESPONSE, PRODUCT_RESPONSE, USER_RESPONSE, USER

from custom_api_response import custom_error_response


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
            jsonschema.validate(request.data, PRODUCT_SCHEMA)
            color = request.data['specification']['color']
            storage = request.data['specification']['storage']
            product = Product.objects.filter(is_active=TRUE, name=request.data['name'], specification={
                "color": color, "storage": storage})
            if product:
                return custom_error_response('specification',
                                             'product with this specification already exists', 400)
            created_by = User.objects.get(id=request.headers.get('user-id'))
            product_serializer = self.get_serializer(data=request.data)
            product_serializer.is_valid(raise_exception=TRUE)
            product = product_serializer.save(created_by=created_by)
            product_response = ProductResponseSerializer(product)
            logger.info('product successfully created')
            return JsonResponse(product_response.data, status=status.HTTP_201_CREATED)

        except jsonschema.exceptions.ValidationError as ex:
            title = re.findall("'([^']*)'", ex.message)
            logger.error(f'Failed to validate the schema')
            return custom_error_response(title[0], ex.message, 400)

        except ValidationError as ex:
            logger.error(f'{ex} has occurred')
            for title, message in ex.get_full_details().items():
                return custom_error_response(title, message[0].get('message'), 400)

        except User.DoesNotExist:
            logger.error(f'No data found for the user of id {request.headers.get("user-id")}')
            return custom_error_response(USER, f'{USER_RESPONSE} {request.headers.get("user-id")}',400)
        except ValueError as ex:
            logger.error(f'Invalid value for the user id {request.headers.get("user-id")}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(f'{ex} has occurred')
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
            products = Product.objects.filter(is_active=TRUE)
            logger.info('list of products successfully retrieved')
            if products:
                product_serializer = ProductResponseSerializer(products, many=TRUE)
                return JsonResponse({PRODUCT: product_serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.error(PRODUCT_LIST_RESPONSE)
                return custom_error_response(PRODUCT, PRODUCT_LIST_RESPONSE,400)

        except Exception as ex:
            logger.error(PRODUCT_LIST_RESPONSE)
            return custom_error_response(PRODUCT, ex.args[0], 400)

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
            instance.updated_by = Product.objects.get(Product, is_active=TRUE, id=updated_by)
            if instance.updated_by:
                product_serializer = self.get_serializer(instance, data=request.data)
                product_serializer.is_valid(raise_exception=TRUE)
                self.perform_update(product_serializer)
                return JsonResponse(product_serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(PRODUCT_RESPONSE)
                return custom_error_response(PRODUCT, PRODUCT_RESPONSE, 400)
        except Product.DoesNotExist as ex:
            logger.error(f'{PRODUCT_RESPONSE} {kwargs.get("pk")}')
            return custom_error_response(PRODUCT, ex.args[0], 400)

        except ValueError as ex:
            logger.error(ex.args[0])
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(PRODUCT_RESPONSE)
            return custom_error_response(PRODUCT, ex.args[0], 400)


class ProductUpdateViewSet(APIView):
    """
     A view set that provides `update()` action for the product model instance
    """

    @staticmethod
    def delete(request, product_id=None):
        logger.info('entering the module to soft delete the data')
        """
        This method is used to delete the product object of the instance
        :param request: data of the product object
        :param product_id: id of the required product
        :return: json response of the successful deletion message or error response message
        """
        try:
            product = Product.objects.get(id=product_id)
            if product.is_active:
                product.is_active = FALSE
                product.save()
                return JsonResponse({MESSAGE: 'product successfully deleted'}, status=status.HTTP_200_OK)
            return JsonResponse({MESSAGE: f'{PRODUCT_RESPONSE} {product_id}'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            logger.error(f'{PRODUCT_RESPONSE} {product_id}')
            return custom_error_response(PRODUCT, f'{PRODUCT_RESPONSE} {product_id}', 400)
        except ValueError as ex:
            logger.error(ex.args[0])
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(PRODUCT, ex.args[0], 400)
