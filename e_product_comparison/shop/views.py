import jsonschema
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import User

from .models import Shop
from .serializers import ShopDetailsSerializer, ShopResponseSerializer
from .shop_logger import logger
from user.serilalizers import UserResponseSerializer

from e_product_comparison.myconstants import TRUE, FALSE, MESSAGE, SHOP_SCHEMA


class ShopViewSet(ModelViewSet):
    logger.info('into the shop module')

    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the shop model instance
    """

    queryset = Shop.objects.all()
    serializer_class = ShopDetailsSerializer

    def create(self, request, *args, **kwargs):
        logger.info('Entering the shop creation module')
        """
        This method is used to create the shop object from the request
        :param request: data object for the shop instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the json response of the shop object or error response of the same
        """
        try:
            jsonschema.validate(request.data, SHOP_SCHEMA)
            user = get_object_or_404(User, id=request.data['user'], is_active=TRUE)
            user_data = UserResponseSerializer(user)
            if user_data.data['is_seller']:
                shop_product_serializer = self.get_serializer(data=request.data)
                shop_product_serializer.is_valid(raise_exception=TRUE)
                shop_product_serializer.save(created_by=user)
                logger.info('shop successfully created')
                return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({MESSAGE: 'Register as a seller to add your shop'},
                                    status=status.HTTP_400_BAD_REQUEST)
        except jsonschema.exceptions.ValidationError as ex:
            logger.error(f'Failed to validate the schema')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f'No data found for the user of id {request.headers.get("user-id")}')
            return JsonResponse({MESSAGE: 'No data found for the users'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the field pk {request.headers.get("user-id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.info('entering the shop updating module')
        """
        This method is used to update the shop object
        :param request: data to update the shop object of the instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the updated shop object as json response or error message in the same format
        """
        try:
            updated_by = request.data['user']
            instance = self.get_object()
            print('0: ', instance)
            instance.updated_by = get_object_or_404(User, id=updated_by)
            print('1: ', instance)
            shop_detail_serializer = self.get_serializer(instance, data=request.data)
            shop_detail_serializer.is_valid(raise_exception=TRUE)
            self.perform_update(shop_detail_serializer)
            logger.info('shop successfully updated')
            return JsonResponse(shop_detail_serializer.data)
        except Shop.DoesNotExist:
            logger.error(f'No shop found for the id {request.headers.get("id")}')
            return JsonResponse({MESSAGE: f'No shop found for the id {request.headers.get("id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the field pk {request.headers.get("id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        logger.info('Module to list the entire shop data')
        """
        This method lists all the shops
        :param request: request to get all objects
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: Returns the list of all shop in Json response object
        """
        try:
            shop = get_list_or_404(Shop, is_active=TRUE)
        except Shop.DoesNotExist:
            logger.error('No data found for shop')
            return JsonResponse({MESSAGE: 'No data found for the shop'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            shop_serializer = ShopResponseSerializer(shop, many=TRUE)
            return JsonResponse({'user': shop_serializer.data},
                                status=status.HTTP_200_OK)

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
            data = Shop.objects.get(is_active=TRUE, id=shop_id)
        except Shop.DoesNotExist:
            logger.error(f'No data found for the shop of id {shop_id}')
            return JsonResponse({MESSAGE: f'No data found for the user of id {shop_id}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {shop_id}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(f'user object found for the id ')
            shop_serializer = ShopResponseSerializer(data)
            return JsonResponse(shop_serializer.data, status=status.HTTP_200_OK)


class ShopDetailsUpdateView(APIView):
    logger.info('entering the module to soft delete the shop')
    """
     A view set that provides `update()` action for the shop model instance
    """

    @staticmethod
    def patch(request, pk=None):
        """
        This method is used to delete the shop
        :param request: To delete the shop by changing its active status
        :param pk: id of the shop
        :return:Response message of successfully deletion or error response
        """
        try:
            shop_details = get_object_or_404(Shop, id=pk)
            shop_data = {'is_active': FALSE}
            shop_details_serializer = ShopDetailsSerializer(shop_details, data=shop_data, partial=TRUE)
            if shop_details_serializer.is_valid():
                shop_details_serializer.save()
                return JsonResponse(shop_details_serializer.data, status=status.HTTP_200_OK)
            return JsonResponse({MESSAGE: 'Shop details deletion failed'}, status=status.HTTP_204_NO_CONTENT)
        except Shop.DoesNotExist:
            logger.error(f'No shop found for the id {pk}')
            return JsonResponse({MESSAGE: f'No shop found for the id {pk}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the field pk {pk}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
