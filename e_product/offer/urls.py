from django.urls import path, include
from rest_framework.routers import DefaultRouter

from offer import views

router = DefaultRouter()
router.register('api/v1/product/offer', views.OfferViewSet)


urlpatterns = [
    path('api/v1/product/view/<int:product_id>', views.OfferView.as_view()),
    path('api/v1/product/view/<str:name>', views.ViewOffersByProductName.as_view()),
    path('api/v1/shop-product-update/<int:shop_product_id>', views.OfferUpdateViewSet.as_view()),
    path('', include(router.urls))
]
