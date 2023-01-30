import re

import jsonschema
from custom_api_response import custom_error_response
from django.http import JsonResponse
from e_product_comparison.myconstants import MESSAGE, USER_RESPONSE, USER
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import User

from .models import Product
from .product_constants import TRUE, FALSE, PRODUCT, PRODUCT_RESPONSE, PRODUCT_LIST_RESPONSE, PRODUCT_SCHEMA, ERROR_FORMAT
from .product_logger import logger
from .serializers import ProductSerializer, ProductResponseSerializer


class ProductViewSet(ModelViewSet):
    logger.info('entering the product view set module')
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the product model instance
    """
    queryset = Product.objects.filter(is_active=TRUE)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the product objects from the request instance
        :param request: product instance to create a new product object
        :param args: extra positional argument for product object
        :param kwargs: extra keyword argument for product object
        :return: jsonobject of the newly created product or error response as required
        """
        try:
            logger.info('into the product creation module')
            jsonschema.validate(request.data, PRODUCT_SCHEMA)
            product = Product.objects.filter(is_active=TRUE, name=request.data['name'].upper(),
                                             specification__contains={
                                                 'color': request.data['specification']['color'].upper(),
                                                 'storage': request.data['specification']['storage'].upper()})
            if product:
                logger.error('product with this specification already exists')
                return JsonResponse({'specification': 'product with this specification already exists'},
                                    status=status.HTTP_200_OK)
            logger.info('creating a new product')
            created_by = User.objects.get(is_active=TRUE, id=request.headers.get('user-id'))
            logger.info('user is found and is active')
            product_serializer = self.get_serializer(data=request.data)
            product_serializer.is_valid(raise_exception=TRUE)
            product = product_serializer.save(created_by=created_by)
            product_response = ProductResponseSerializer(product)
            logger.info('product successfully created')
            return JsonResponse(product_response.data, status=status.HTTP_201_CREATED)

        except jsonschema.exceptions.ValidationError as ex:
            title = re.findall(ERROR_FORMAT, ex.message)
            logger.error(f'Failed to validate the schema')
            return custom_error_response(title[0], ex.message, 400)
        except ValidationError as ex:
            logger.error(f'123: {ex} has occurred')
            for title, message in ex.get_full_details().items():
                return custom_error_response(title, message[0].get('message'), 400)
        except User.DoesNotExist:
            logger.error(f'No data found for the user of id {request.headers.get("user-id")}')
            return custom_error_response(USER, f'{USER_RESPONSE} {request.headers.get("user-id")}', 400)
        except ValueError as ex:
            logger.error(f'Invalid value for the user id {request.headers.get("user-id")}')
            title = re.findall(ERROR_FORMAT, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)
        except Exception as ex:
            logger.error(f'1: {ex.args} has occurred')
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
            if products:
                logger.info('list of products successfully retrieved')
                product_serializer = ProductResponseSerializer(products, many=TRUE)
                return JsonResponse({PRODUCT: product_serializer.data}, status=status.HTTP_200_OK)
            logger.error(PRODUCT_LIST_RESPONSE)
            return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_200_OK)

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
            instance.updated_by = User.objects.get(id=updated_by)
            if instance.updated_by:
                product_serializer = self.get_serializer(instance, data=request.data)
                product_serializer.is_valid(raise_exception=TRUE)
                self.perform_update(product_serializer)
                return JsonResponse(product_serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(PRODUCT_RESPONSE)
                return custom_error_response(PRODUCT, PRODUCT_RESPONSE, 400)
        except User.DoesNotExist as ex:
            logger.error(f'{PRODUCT_RESPONSE} {kwargs.get("pk")}')
            return custom_error_response(PRODUCT, ex.args[0], 400)

        except ValueError as ex:
            logger.error(ex.args[0])
            title = re.findall(ERROR_FORMAT, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(PRODUCT_RESPONSE)
            return custom_error_response(PRODUCT, ex.args[0], 400)


class DeleteProduct(APIView):
    """
     A view set that provides `update()` action for the product model instance
    """
    def delete(self, request):
        logger.info('entering the module to soft delete the data')
        """
        This method is used to delete the product object of the instance
        :param request: data of the product object
        :param product_id: id of the required product
        :return: json response of the successful deletion message or error response message
        """
        try:
            logger.info('fetching the product to delete')
            product = Product.objects.get(id=self.request.query_params.get('product-id'))
            if product and product[0].is_active:
                logger.info('product is found to be active')
                product[0].is_active = FALSE
                updated_by = User.objects.filter(is_active=TRUE, id=request.headers.get('user'))
                if updated_by:
                    product[0].updated_by = updated_by[0]
                    product[0].save()
                    logger.info(f'{product[0]}successfully deleted')
                    return JsonResponse({MESSAGE: 'product successfully deleted'}, status=status.HTTP_200_OK)
                logger.info(f'{USER_RESPONSE} {request.headers.get("user")}')
                return JsonResponse({MESSAGE: f'{USER_RESPONSE} {request.headers.get("user")}'})
            logger.info(f'{PRODUCT_RESPONSE} {self.request.query_params.get("product-id")}')
            return JsonResponse({MESSAGE: f'{PRODUCT_RESPONSE} {self.request.query_params.get("product-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(ex.args[0])
            title = re.findall(ERROR_FORMAT, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)
        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(PRODUCT, ex.args[0], 400)


class ViewProducts(APIView):
    """
         A view set that provides `get()` action for the offer model instance
        """

    def get(self, request):
        try:
            if self.request.query_params.get("category"):
                products = Product.objects.filter(is_active=TRUE,
                                                  category_type=self.request.query_params.get("category"))
                logger.info(f'products found for category {self.request.query_params.get("category")}')
            else:
                logger.info('finding the list of all products')
                products = Product.objects.filter(is_active=TRUE)

            if products:
                products_response = ProductResponseSerializer(products, many=TRUE)
                logger.info(f'list of products found')
                return JsonResponse({PRODUCT: products_response.data}, status=status.HTTP_200_OK)
            logger.error(PRODUCT_LIST_RESPONSE)
            return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(PRODUCT, ex.args[0], 400)
