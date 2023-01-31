import re

import jsonschema
from custom_api_response import custom_error_response
from django.http import JsonResponse
from product.models import Product
from product.serializers import ProductResponseSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from shop.models import Shop
from user.models import User

from .models import Offer
from .offer_constants import TRUE, FALSE, MESSAGE, OFFER, OFFER_RESPONSE, OFFER_LIST_RESPONSE, COLOR, STORAGE, \
    SPECIFICATION, ID, NAME, OFFER_SCHEMA, VALUE_ERROR_PATTERN, USER_RESPONSE, PRODUCT, PRODUCT_RESPONSE, \
    PRODUCT_LIST_RESPONSE, SHOP, SHOP_RESPONSE
from .offer_logger import logger
from .serializers import OfferSerializer, OfferResponseSerializer


class OfferViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
     'list()` actions for the shop_product model instance
    """
    queryset = Offer.objects.filter(is_active=TRUE)
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the shop_product object for the instance
        :param request: data to create new shop_product instance
        :param args: extra positional argument for shop_product object
        :param kwargs: extra keyword argument for shop_product object
        :return: returns the json response of the created object or error response in the same format
        """

        try:
            jsonschema.validate(request.data, OFFER_SCHEMA)
            offer = Offer.objects.filter(is_active=TRUE, product=request.data['product'], shop=request.data['shop'],
                                         actual_price=request.data['actual_price'],
                                         offer_percentage=request.data['offer_percentage'])
            if offer:
                logger.error('this offer already exists')
                return JsonResponse({OFFER: 'This offer already exists'}, status=status.HTTP_200_OK)

            logger.info('entering the offer creation module')
            product = Product.objects.filter(is_active=TRUE, id=request.data[PRODUCT])
            if product:
                logger.info('Product is available ')
                shop = Shop.objects.filter(is_active=TRUE, id=request.data[SHOP])
                if shop:
                    logger.info('shop is available')
                    user = User.objects.get(is_active=TRUE, id=request.headers.get('user-id'))
                    if user:
                        logger.info('user is found')
                        offer_serializer = self.get_serializer(data=request.data)
                        logger.info('offer is serialized')
                        offer_serializer.is_valid(raise_exception=TRUE)
                        logger.info('serialized offer is valid')
                        offer = offer_serializer.save(created_by=user)
                        logger.info('setting the created by')
                        offer_response = OfferResponseSerializer(offer)
                        logger.info('offer successfully created')
                        return JsonResponse(offer_response.data, status=status.HTTP_201_CREATED)
                    logger.info(f'{USER_RESPONSE} {request.headers.get("user-id")}')
                    return custom_error_response('user', f'{USER_RESPONSE} {request.headers.get("user-id")}', 400)
                logger.info(f'{SHOP_RESPONSE} {request.data[SHOP]}')
                return custom_error_response(SHOP, f'{SHOP_RESPONSE} {request.data[SHOP]}', 400)
            logger.info(f'{PRODUCT_RESPONSE} {request.data[PRODUCT]}')
            return custom_error_response(PRODUCT, f'{PRODUCT_RESPONSE} {request.data[PRODUCT]}', 400)

        except User.DoesNotExist:
            logger.error(f'User does not exist for the id {request.headers.get("user-id")}')
            return JsonResponse({'user': f'User does not exist for the id {request.headers.get("user-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {request.headers.get("user-id")}')
            title = re.findall(VALUE_ERROR_PATTERN, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the shop_product instance object
        :param request: id of the shop_product object to be updated
        :param args: extra positional argument for shop_product object
        :param kwargs: extra keyword argument for shop_product object
        :return: returns the json response of the updated shop_product object or error response in the same
        """
        try:
            logger.info('entering the offer updating module')
            user_id = request.headers.get('user-id')
            instance = self.get_object()
            instance.updated_by = User.objects.get(is_active=TRUE, id=user_id)
            offer_serializer = self.get_serializer(instance, data=request.data)
            offer_serializer.is_valid(raise_exception=TRUE)
            self.perform_update(offer_serializer)
            logger.info('offer successfully updated')
            return JsonResponse(offer_serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f'User does not exist for the id {request.headers.get("user-id")}')
            return JsonResponse({'user': f'User does not exist for the id {request.headers.get("user-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error(f'Invalid value for the key id {request.headers.get(ID)}')
            title = re.findall(VALUE_ERROR_PATTERN, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)


class OfferUpdateViewSet(APIView):
    """
     A view set that provides `update()` action for the offer model instance
    """
    def delete(self, request):
        """
        This method is used to delete the offer instance
        :param request: Data's of the offer instance
        :param offer_id: id of the offer object
        :return: returns the updated response message
        """
        try:
            logger.info('finding offers to delete')
            offer = Offer.objects.filter(id=self.request.query_params.get("offer-id"))
            if offer and offer[0].is_active:
                logger.info('offer is found to be active')
                offer[0].is_active = FALSE
                updated_by = User.objects.filter(is_active=TRUE, id=request.headers.get("user"))
                if updated_by:
                    offer[0].updated_by = updated_by[0]
                    offer[0].save()
                    logger.info('offer successfully deleted')
                    return JsonResponse({MESSAGE: 'offer successfully deleted'}, status=status.HTTP_200_OK)
                logger.info()
                return JsonResponse({MESSAGE: f'{USER_RESPONSE} {request.headers.get("user")}'})
            return JsonResponse({MESSAGE: f'{OFFER_RESPONSE} {self.request.query_params.get("offer-id")}'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            logger.error('Invalid value for the key')
            title = re.findall(VALUE_ERROR_PATTERN, ex.args[0])
            return custom_error_response(title[0], ex.args[0], 400)

        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)


class ViewOffers(APIView):
    """
         A view set that provides `get()` action for the offer model instance
        """
    @staticmethod
    def get(request):
        if request.data:
            try:
                if ID in request.data:
                    logger.info(f'finding the product of id {request.data[ID]}')
                    product = Product.objects.filter(id=request.data[ID], is_active=TRUE)
                    logger.info(f'product found for the id {request.data[ID]}')

                elif NAME and SPECIFICATION in request.data:
                    logger.info(f'finding the product of name {request.data[NAME]}')
                    if COLOR in request.data[SPECIFICATION] and STORAGE in request.data[SPECIFICATION]:
                        logger.info('finding product with the given specification')
                        product = Product.objects.filter(name=request.data[NAME].upper(), specification__contains={
                            COLOR: request.data[SPECIFICATION][COLOR].upper(),
                            STORAGE: request.data[SPECIFICATION][STORAGE].upper()}, is_active=TRUE)
                        logger.info(f'product found for the name {request.data[NAME]}')
                    elif COLOR in request.data[SPECIFICATION] and STORAGE not in request.data[SPECIFICATION]:
                        products = Product.objects.filter(name=request.data[NAME].upper(), specification__contains={
                            COLOR: request.data[SPECIFICATION][COLOR].upper()}, is_active=TRUE)
                        if products:
                            logger.info('all products found')
                            products_response = ProductResponseSerializer(products, many=TRUE)
                            return JsonResponse({PRODUCT: products_response.data}, status=status.HTTP_200_OK)
                        return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_200_OK)
                    elif STORAGE in request.data[SPECIFICATION] and COLOR not in request.data[SPECIFICATION]:
                        products = Product.objects.filter(name=request.data[NAME].upper(), specification__contains={
                            STORAGE: request.data[SPECIFICATION][STORAGE].upper()}, is_active=TRUE)
                        if products:
                            logger.info('all products found')
                            products_response = ProductResponseSerializer(products, many=TRUE)
                            return JsonResponse({PRODUCT: products_response.data}, status=status.HTTP_200_OK)
                        return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_200_OK)
                elif NAME in request.data and SPECIFICATION not in request.data[NAME]:
                    products = Product.objects.filter(name__contains=request.data[NAME].upper(), is_active=TRUE)
                    if products:
                        logger.info('all products found')
                        products_response = ProductResponseSerializer(products, many=TRUE)
                        return JsonResponse({PRODUCT: products_response.data}, status=status.HTTP_200_OK)
                    return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_200_OK)

                if product:
                    product_serializer = ProductResponseSerializer(product[0])
                    offers = Offer.objects.filter(product_id=product[0].id, is_active=TRUE)
                    if offers:
                        offer_serializer = OfferResponseSerializer(offers, many=TRUE)
                        response = {PRODUCT: product_serializer.data, OFFER: offer_serializer.data}
                        return JsonResponse(response, status=status.HTTP_200_OK)
                    response = {PRODUCT: product_serializer.data, OFFER: OFFER_LIST_RESPONSE}
                    return JsonResponse(response, status=status.HTTP_200_OK)
                return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_400_BAD_REQUEST)
            except TypeError as ex:
                logger.error(f'Invalid value for the key id {product.id}')
                title = re.findall("'([^']*)'", ex.args[0])
                return custom_error_response(title[0], ex.args[0], 400)
            except Exception as ex:
                logger.error(ex.args[0])
                return custom_error_response(OFFER, ex.args[0], 400)

        try:
            logger.info('finding all the offers')
            products = Product.objects.filter(is_active=TRUE)
            if products:
                logger.info('all offers found')
                products_response = ProductResponseSerializer(products, many=TRUE)
                return JsonResponse({PRODUCT: products_response.data}, status=status.HTTP_200_OK)
            return JsonResponse({PRODUCT: PRODUCT_LIST_RESPONSE}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(ex.args[0])
            return custom_error_response(OFFER, ex.args[0], 400)
