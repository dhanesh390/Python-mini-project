from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from product.serializers import ProductResponseSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import User

from .models import Offer
from .serializers import OfferSerializer, OfferResponseSerializer
from .offer_logger import logger
from product.models import Product
from shop.models import Shop
from e_product_comparison.myconstants import TRUE, FALSE, MESSAGE


class OfferViewSet(ModelViewSet):
    logger.info('into the offer view set')
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
     'list()` actions for the shop_product model instance
    """
    queryset = Offer.objects.filter(is_active=TRUE)
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        logger.info('entering the offer creation module')
        """
        This method is used to create the shop_product object for the instance
        :param request: data to create new shop_product instance
        :param args: extra positional argument for shop_product object
        :param kwargs: extra keyword argument for shop_product object
        :return: returns the json response of the created object or error response in the same format
        """

        try:
            product = Product.objects.get(id=request.data["product"], is_active=TRUE)
            shop = Shop.objects.get(id=request.data["shop"], is_active=TRUE)
            shop_product_serializer = self.get_serializer(data=request.data)
            shop_product_serializer.is_valid(raise_exception=TRUE)
            if request.headers.get('user-id'):
                created_by = User.objects.get(id=request.headers.get('user-id'))
                shop_product_serializer.save(created_by=created_by)
                logger.info('offer successfully created')
            elif request.data['user_id']:
                created_by = User.objects.get(id=request.data['user_id'])
                shop_product_serializer.save(created_by=created_by)
                logger.info('offer successfully created')
            return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            logger.error(f'User does not exist for the id {request.headers.get("user-id")}')
            return JsonResponse({'user': f'User does not exist for the id {request.headers.get("user-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            logger.error(f'product for the id {request.data["product"]} does not exist')
            return JsonResponse({'product': f'product for the id {request.data["product"]} does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Shop.DoesNotExist:
            logger.error(f'shop for the id {request.data["shop"]} does not exist')
            return JsonResponse({'shop': f'shop for the id {request.data["shop"]} does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {request.headers.get("user-id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.info('entering the offer updating module')
        """
        This method is used to update the shop_product instance object
        :param request: id of the shop_product object to be updated
        :param args: extra positional argument for shop_product object
        :param kwargs: extra keyword argument for shop_product object
        :return: returns the json response of the updated shop_product object or error response in the same
        """
        try:
            updated_by = request.headers.get('id')
            print('1: ', updated_by)
            instance = self.get_object()
            print('2: ', instance)
            instance.updated_by = get_object_or_404(User, is_active=TRUE, id=updated_by)
            print('3: ', instance.updated_by)
            shop_product_serializer = self.get_serializer(instance, data=request.data)
            shop_product_serializer.is_valid(raise_exception=TRUE)
            self.perform_update(shop_product_serializer)
            logger.info('offer successfully updated')
            return JsonResponse(shop_product_serializer.data)
        except User.DoesNotExist:
            logger.error(f'User does not exist for the id {request.headers.get("user-id")}')
            return JsonResponse({'user': f'User does not exist for the id {request.headers.get("user-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {request.headers.get("id")}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class OfferUpdateViewSet(APIView):
    logger.info('entering the offer updating view set')
    """
     A view set that provides `update()` action for the offer model instance
    """

    @staticmethod
    def patch(request, offer_id=None):
        logger.info('entering the module to soft delete the offers')
        """
        This method is used to delete the offer instance
        :param request: Data's of the offer instance
        :param offer_id: id of the offer object
        :return: returns the updated response message
        """
        try:
            shop_product = get_object_or_404(Offer, id=offer_id)
            shop_product_data = {'is_active': FALSE}
            shop_product_serializer = OfferResponseSerializer(shop_product, data=shop_product_data, partial=TRUE)
            if shop_product_serializer.is_valid():
                shop_product_serializer.save()
                return JsonResponse({MESSAGE: 'offer successfully deleted '}, status=status.HTTP_200_OK)
            return JsonResponse({MESSAGE: "wrong parameters"}, status=status.HTTP_400_BAD_REQUEST)
        except Offer.DoesNotExist:
            logger.error(f'offer does not exist for the id {offer_id}')
            return JsonResponse({'user': f'User does not exist for the id {offer_id}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {offer_id}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class OfferView(APIView):
    logger.info('entering offer request view set by id')
    """
     A view set that provides `get()` action for the offer model instance
    """

    @staticmethod
    def get(request, product_id=None):
        try:
            shop_product = get_list_or_404(Offer, product_id=product_id, is_active=TRUE)
            shop_product_serializer = OfferResponseSerializer(shop_product, many=TRUE)
            product = get_object_or_404(Product, id=product_id)
            product_serializer = ProductResponseSerializer(product)
            response = {'product': product_serializer.data, 'offers': shop_product_serializer.data}
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f'No product found for the id {product_id}')
            return JsonResponse({'product': f'No product found for the id {product_id}'})
        except Offer.DoesNotExist:
            logger.error(f'offer does not exist for the product of id {product_id}')
            return JsonResponse({'user': f'User does not exist for the product of id {product_id}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {product_id}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class ViewOffersByProductName(APIView):
    """
         A view set that provides `get()` action for the offer model instance
        """

    @staticmethod
    def get(request, name=None):
        try:
            product = get_object_or_404(Product, name=name, is_active=TRUE)
            product_serializer = ProductResponseSerializer(product)
            offers = get_list_or_404(Offer, product_id=product.id, is_active=TRUE)
            offer_serializer = OfferResponseSerializer(offers, many=TRUE)
            response = {'product': product_serializer.data, 'offers': offer_serializer.data}
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f'No product found for the name {name}')
            return JsonResponse({'product': f'No product found for the name {name}'})
        except Offer.DoesNotExist:
            logger.error(f'offer does not exist for the product of name {name}')
            return JsonResponse({'user': f'User does not exist for the product of id {name}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key name {name}')
            return JsonResponse({MESSAGE: ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
