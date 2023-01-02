from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('users', views.UserViewSet)


urlpatterns = [
    path('shop_details', views.ShopDetailsCrud.as_view()),
    path('shop_details/<int:pk>/', views.ShopDetailsCrud.as_view()),
    path('update_user/<int:pk>', views.UserUpdateView.as_view()),
    path('', include(router.urls))

]
