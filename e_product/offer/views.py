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


class OfferViewSet(ModelViewSet):
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

        try:
            created_by = User.objects.get(id=request.headers.get('user-id'))
            product = Product.objects.get(id=request.data["product"], is_active=True)
            shop = Shop.objects.get(id=request.data["shop"], is_active=True)
            shop_product_serializer = self.get_serializer(data=request.data)
            shop_product_serializer.is_valid(raise_exception=True)
            shop_product_serializer.save(created_by=created_by)
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


class OfferUpdateViewSet(APIView):
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


class OfferView(APIView):
    """
     A view set that provides `get()` action for the offer model instance
    """

    @staticmethod
    def get(request, product_id=None):
        try:
            shop_product = get_list_or_404(Offer, product_id=product_id, is_active=True)
            shop_product_serializer = OfferResponseSerializer(shop_product, many=True)
            product = get_object_or_404(Product, id=product_id)
            product_serializer = ProductResponseSerializer(product)
            response = {'product': product_serializer.data, 'shop_product': shop_product_serializer.data}
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f'No product found for the id {product_id}')
            return JsonResponse({'product': f'No product found for the id {product_id}'})


class ViewOffersByProductName(APIView):
    """
         A view set that provides `get()` action for the offer model instance
        """
    @staticmethod
    def get(request, name=None):
        try:
            product = get_object_or_404(Product, name=name, is_active=True)
            product_serializer = ProductResponseSerializer(product)
            offers = get_list_or_404(Offer, product_id=product.id, is_active=True)
            offer_serializer = OfferResponseSerializer(offers, many=True)
            response = {'product': product_serializer.data, 'offers': offer_serializer.data}
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f'No product found for the name {name}')
            return JsonResponse({'product': f'No product found for the name {name}'})
