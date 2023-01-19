from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register('api/v1/product', views.ProductViewSet)

urlpatterns = [
    path('api/v1/product-update/<int:product_id>', views.ProductUpdateViewSet.as_view()),
    path('', include(router.urls))
]
