from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop import views

router = DefaultRouter()
router.register('api/v1/shop', views.ShopViewSet)

urlpatterns = [
    path('api/v1/shop/update/<int:pk>', views.ShopDetailsUpdateView.as_view()),
    path('', include(router.urls))
]