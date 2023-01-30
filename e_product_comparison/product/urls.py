from django.urls import path, include
from product import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/v1/product', views.ProductViewSet)

urlpatterns = [
    path('api/v1/product/update/?<int:product_id>', views.DeleteProduct.as_view()),
    path('api/v1/product/view/category', views.ViewProducts.as_view()),
    path('', include(router.urls))
]
