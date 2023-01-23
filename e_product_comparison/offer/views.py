import re

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
from e_product_comparison.myconstants import TRUE, FALSE, MESSAGE, USER, OFFER, PRODUCT, OFFER_LIST_RESPONSE, OFFER_RESPONSE, PRODUCT_RESPONSE, PRODUCT_LIST_RESPONSE

from custom_api_response import custom_error_response


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
            return custom_error_response({'shop': f'shop for the id {request.data["shop"]} does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {request.headers.get("user-id")}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)

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
            param = self.request.query_params
            user_id = param.get('id')
            print('id: ', user_id)
            # print('id: ', user_id)
            # updated_by = request.headers.get('id')
            instance = self.get_object()
            instance.updated_by = get_object_or_404(User, is_active=TRUE, id=user_id)
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
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)


class OfferUpdateViewSet(APIView):
    logger.info('entering the offer updating view set')
    """
     A view set that provides `update()` action for the offer model instance
    """

    @staticmethod
    def delete(request, offer_id=None):
        logger.info('entering the module to soft delete the offers')
        """
        This method is used to delete the offer instance
        :param request: Data's of the offer instance
        :param offer_id: id of the offer object
        :return: returns the updated response message
        """
        try:
            offer = get_object_or_404(Offer, id=offer_id)
            if offer.is_active:
                offer.is_active = FALSE
                offer.save()
                return JsonResponse({MESSAGE: 'offer successfully deleted '}, status=status.HTTP_200_OK)
            return JsonResponse({MESSAGE: "No offers found"}, status=status.HTTP_400_BAD_REQUEST)
        except Offer.DoesNotExist:
            logger.error(f'offer does not exist for the id {offer_id}')
            return JsonResponse({'user': f'User does not exist for the id {offer_id}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {offer_id}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)


class OfferView(APIView):
    logger.info('entering offer request view set by id')
    """
     A view set that provides `get()` action for the offer model instance
    """

    @staticmethod
    def get(request, product_id=None):
        try:
            logger.info(f'finding the product {product_id}')
            product = Product.objects.get(is_active=TRUE, id=product_id)
            logger.info(f'product found for the id {product_id}')
            product_serializer = ProductResponseSerializer(product)
            # print('id: ', request.get('id'))
            logger.info(f'finding offers for products using product id {product_id}')
            offer = get_list_or_404(Offer, product_id=product_id, is_active=TRUE)
            logger.info(f'offers found for the product {product_id}')
            offer_serializer = OfferResponseSerializer(offer, many=TRUE)

            response = {'product': product_serializer.data, 'offers': offer_serializer.data}
            return JsonResponse(response.items(), status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f'{PRODUCT_RESPONSE} {product_id}')
            return custom_error_response(PRODUCT, f'{PRODUCT_RESPONSE} {product_id}', 400)
        except Offer.DoesNotExist:
            logger.error(f'{OFFER_RESPONSE} of the product {product_id}')
            return custom_error_response(OFFER, f'{OFFER_RESPONSE} of the product {product_id}', 400)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {product_id}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)


class ViewOffersByProductName(APIView):
    """
         A view set that provides `get()` action for the offer model instance
        """

    @staticmethod
    def get(request, name=None):
        try:
            logger.info(f'finding the product {name}')
            product = Product.objects.filter(name=name, is_active=TRUE)
            logger.info(f'product found for the name {name}')
            if product:
                product_serializer = ProductResponseSerializer(product)
                logger.info(f'finding offers for products using product name {name}')
            else:
                logger.error(PRODUCT_RESPONSE)
                return custom_error_response(PRODUCT, PRODUCT_LIST_RESPONSE, 400)

            offers = Offer.objects.filter(product_id=product.id, is_active=TRUE)
            if offers:
                logger.info(f'offers found for the product {name}')
                offer_serializer = OfferResponseSerializer(offers, many=TRUE)
            else:
                logger.error(OFFER_LIST_RESPONSE)
                return custom_error_response(OFFER, OFFER_LIST_RESPONSE, 400)
            response = {'product': product_serializer.data, 'offers': offer_serializer.data}
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f'{PRODUCT_RESPONSE} {product.id}')
            return custom_error_response(PRODUCT, f'{PRODUCT_RESPONSE} {name}', 400)
        except Offer.DoesNotExist:
            logger.error(f'{OFFER_RESPONSE} of the product {product.id}')
            return custom_error_response(OFFER, f'{OFFER_LIST_RESPONSE} {name}', 400)
        except ValueError as ex:
            logger.error(f'Invalid value for the key name {name}')
            title = re.findall("'([^']*)'", ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)
