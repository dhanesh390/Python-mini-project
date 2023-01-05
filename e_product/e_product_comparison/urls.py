from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('api/v1/user', views.UserViewSet)
router.register('api/v1/product', views.ProductViewSet)
router.register('api/v1/shop', views.ShopDetailsViewSet)
router.register('api/v1/shop-product', views.ShopProductViewSet)

urlpatterns = [
    path('api/v1/update-user/<int:pk>', views.UserUpdateView.as_view()),
    path('api/v1/product-update/<int:product_id>', views.ProductUpdateViewSet.as_view()),
    path('api/v1/shop-product-view/<int:product_id>', views.ShopProductView.as_view()),
    path('api/v1/shop-product-update/<int:shop_product_id>', views.ShopProductUpdateViewSet.as_view()),
    path('api/v1/shop/update/<int:pk>', views.ShopDetailsUpdateView.as_view()),
    path('', include(router.urls))
]
