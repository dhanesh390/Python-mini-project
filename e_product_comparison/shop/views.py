import re

import jsonschema
from custom_api_response import custom_error_response
from django.http import JsonResponse
from e_product_comparison.myconstants import USER_RESPONSE, USER, SHOP_LIST_RESPONSE, SHOP_RESPONSE
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import User
from user.serilalizers import UserResponseSerializer

from .models import Shop
from .serializers import ShopDetailsSerializer, ShopResponseSerializer
from .shop_constants import SHOP_SCHEMA, SHOP, SHOP_RESPONSE, SHOP_LIST_RESPONSE, TRUE, FALSE, MESSAGE, ERROR_PATTERN
from .shop_logger import logger


class ShopViewSet(ModelViewSet):
    logger.info('into the shop module')

    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the shop model instance
    """

    queryset = Shop.objects.all()
    serializer_class = ShopDetailsSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the shop object from the request
        :param request: data object for the shop instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the json response of the shop object or error response of the same
        """
        try:
            logger.info('Entering the shop creation module')
            jsonschema.validate(request.data, SHOP_SCHEMA)
            shop = Shop.objects.filter(is_active=TRUE, building_no=request.data['building_no'],
                                       street_name=request.data['street_name'], locality=request.data['locality'],
                                       district=request.data['district'], state=request.data['state'],
                                       country=request.data['country'], pincode=request.data['pincode'])
            if shop:
                logger.error('A shop in this address already exists')
                return JsonResponse({MESSAGE: 'A shop in this already exists'}, status=status.HTTP_400_BAD_REQUEST)
            logger.info('finding user of the shop')
            user = User.objects.get(is_active=TRUE, id=request.data['user'])
            if user:
                logger.info(f'user found for the id {request.data["user"]}')
                user_data = UserResponseSerializer(user)
                if user_data.data['is_seller']:
                    logger.info('user is found to be a seller')
                    shop_serializer = self.get_serializer(data=request.data)
                    shop_serializer.is_valid(raise_exception=TRUE)
                    shop = shop_serializer.save(created_by=user)
                    logger.info('shop successfully created')
                    shop_response = ShopResponseSerializer(shop)
                    return JsonResponse(shop_response.data, status=status.HTTP_201_CREATED)
                return JsonResponse({MESSAGE: 'Register as a seller to add your shop'},
                                    status=status.HTTP_400_BAD_REQUEST)
            logger.error(f'{USER_RESPONSE} {request.data["user"]}')
            return custom_error_response(USER, f'{USER_RESPONSE} {request.data["user"]}', 400)

        except jsonschema.exceptions.ValidationError as ex:
            title = re.findall(ERROR_PATTERN, ex.message)
            logger.error(f'Failed to validate the schema')
            return custom_error_response(title[0], ex.message, 400)
        except User.DoesNotExist:
            logger.error(f'{USER_RESPONSE} {request.data["user"]}')
            return custom_error_response(USER, f'{USER_RESPONSE} {request.data["user"]}', 400)
        except Shop.DoesNotExist:
            logger.error('No data found for the shop')
            return JsonResponse({MESSAGE: 'No data found for the shop'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the field pk {request.headers.get("user-id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(SHOP, ex.args[0], 400)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the shop object
        :param request: data to update the shop object of the instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the updated shop object as json response or error message in the same format
        """
        try:
            logger.info('entering the shop updating module')
            updated_by = request.data['user']
            instance = self.get_object()
            instance.updated_by = User.objects.filter(id=updated_by)
            if instance.updated_by:
                shop_detail_serializer = self.get_serializer(instance, data=request.data)
                shop_detail_serializer.is_valid(raise_exception=TRUE)
                self.perform_update(shop_detail_serializer)
                logger.info('shop successfully updated')
                return JsonResponse(shop_detail_serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(f'{USER_RESPONSE} {updated_by}')
                return custom_error_response(USER, f'{USER_RESPONSE} {updated_by}', 400)
        except Shop.DoesNotExist:
            logger.error(f'{SHOP_RESPONSE} {request.headers.get("id")}')
            return custom_error_response(SHOP, f'{SHOP_RESPONSE} {request.headers.get("id")}', 400)
        except ValueError as ex:
            logger.error(f'Invalid value for the field pk {request.headers.get("id")}')
            title = re.findall(ERROR_PATTERN, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)
        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(SHOP, ex.args[0], 400)

    def list(self, request, *args, **kwargs):
        """
        This method lists all the shops
        :param request: request to get all objects
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: Returns the list of all shop in Json response object
        """
        try:
            logger.info('Module to list the entire shop data')
            shops = Shop.objects.filter(is_active=TRUE)
            logger.info('shop data successfully retrieved')
            if shops:
                shop_serializer = ShopResponseSerializer(shops, many=TRUE)
                return JsonResponse({SHOP: shop_serializer.data}, status=status.HTTP_200_OK)
            logger.error(SHOP_LIST_RESPONSE)
            return JsonResponse({SHOP: SHOP_LIST_RESPONSE}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(ex.args)
            return custom_error_response(SHOP, ex.args[0], 400)

    def retrieve(self, request, *args, **kwargs):
        logger.info('entering the module to retrieve a single shop data')
        """
        This method is used to get the shop data by id
        :param request: request to get shop associated with the request id
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: Returns the shop object as json response or return the exception msg as json response
        """
        shop_id = kwargs.get('pk')
        try:
            logger.info(f'finding the shop object for the id ')
            shop = Shop.objects.filter(is_active=TRUE, id=shop_id)
            if shop:
                logger.info('shop data retrieved')
                shop_serializer = ShopResponseSerializer(shop[0])
                return JsonResponse(shop_serializer.data, status=status.HTTP_200_OK)
            logger.info(f'No shop found for id {shop_id}')
            return JsonResponse({MESSAGE: f'{SHOP_RESPONSE} {shop_id}'}, status=status.HTTP_200_OK)

        except ValueError as ex:
            logger.error(f'Invalid value for the key id {shop_id}')
            title = re.findall(ERROR_PATTERN, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(USER, ex.args[0], 400)


class ShopDetailsUpdateView(APIView):
    """
     A view set that provides `update()` action for the shop model instance
    """

    def delete(self, request):
        """
        This method is used to delete the shop
        :param request: To delete the shop by changing its active status
        :return:Response message of successfully deletion or error response
        """
        try:
            logger.info('entering the module to soft delete the shop')
            shop = Shop.objects.filter(is_active=TRUE, id=self.request.query_params.get('shop-id'))
            if shop and shop[0].is_active:
                logger.info('shop is found to be active')
                shop[0].is_active = FALSE
                updated_by = User.objects.filter(is_active=TRUE, id=request.headers.get('user'))
                if updated_by:
                    shop[0].updated_by = updated_by[0]
                    shop[0].save()
                    logger.info('shop successfully deleted')
                    return JsonResponse({MESSAGE: 'shop successfully deleted'}, status=status.HTTP_200_OK)
                logger.info(f'{USER_RESPONSE} {request.headers.get("user")}')
                return JsonResponse({MESSAGE: f'{USER_RESPONSE} {request.headers.get("user")}'})
            logger.info(f'{SHOP_RESPONSE} {self.request.query_params.get("shop-id")}')
            return JsonResponse({SHOP: f'{SHOP_RESPONSE} {self.request.query_params.get("shop-id")}'},
                                status=status.HTTP_200_OK)

        except ValueError as ex:
            logger.error(f'Invalid value')
            title = re.findall(ERROR_PATTERN, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)
