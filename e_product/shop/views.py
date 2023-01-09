from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import User

from .models import Shop
from .serializers import ShopDetailsSerializer
from .shop_logger import logger


# Create your views here.
class ShopViewSet(ModelViewSet):
    """
     A view set that provides `create()`, `retrieve()`, `update()`,
    `list()` actions for the shop model instance
    """
    logger.info('into the shop module')
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopDetailsSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create the shop object from the request
        :param request: data object for the shop instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the json response of the shop object or error response of the same
        """
        logger.info('Entering the shop creation module')
        print('1: ', request.headers.get('aaa-id'))
        print('2.1: ',request.data)
        created_by = get_object_or_404(User, id=request.headers.get('aaa-id'))
        # created_by = request.headers.get('user_id')
        print('2: ', created_by)
        shop_product_serializer = self.get_serializer(data=request.data)
        print('3: ')
        shop_product_serializer.is_valid(raise_exception=True)
        shop_product_serializer.save(created_by=created_by)
        return JsonResponse(shop_product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the shop object
        :param request: data to update the shop object of the instance
        :param args: extra positional argument for shop object
        :param kwargs: extra keyword argument for shop object
        :return: returns the updated shop object as json response or error message in the same format
        """
        logger.info('entering the shop updating module')
        updated_by = request.headers.get('id')
        instance = self.get_object()
        instance.updated_by = get_object_or_404(User, is_active=True, id=updated_by)
        shop_detail_serializer = self.get_serializer(instance, data=request.data)
        shop_detail_serializer.is_valid(raise_exception=True)
        self.perform_update(shop_detail_serializer)
        return JsonResponse(shop_detail_serializer.data)


class ShopDetailsUpdateView(APIView):
    """
     A view set that provides `update()` action for the shop model instance
    """

    @staticmethod
    def patch(request, pk=None):
        shop_details = get_object_or_404(Shop, id=pk)
        shop_data = {'is_active': False}
        shop_details_serializer = ShopDetailsSerializer(shop_details, data=shop_data, partial=True)
        if shop_details_serializer.is_valid():
            shop_details_serializer.save()
            return JsonResponse(shop_details_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'msg': 'Shop details deletion failed'}, status=status.HTTP_204_NO_CONTENT)