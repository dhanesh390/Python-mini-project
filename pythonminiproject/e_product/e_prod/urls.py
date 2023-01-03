from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserViewSet)
# router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('shop_product', views.ShopProductViewSet)

urlpatterns = [
    path('update_user/<int:pk>', views.UserUpdateView.as_view()),
    # path('update_category', views.CategoryUpdateViewSet.as_view()),
    path('product_update', views.ProductUpdateViewSet.as_view()),
    path('shop_product_view/<int:product_id>', views.ShopProductView.as_view()),
    path('shop_product_update', views.ShopProductUpdateViewSet.as_view()),
    path('shop_details', views.ShopDetailsCrud.as_view()),
    path('shop_details/<int:pk>/', views.ShopDetailsCrud.as_view()),

    path('', include(router.urls))

]
