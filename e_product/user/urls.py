from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register('api/v1/user', views.UserViewSet)

urlpatterns = [
    path('api/v1/update-user/<int:pk>', views.UserUpdateView.as_view()),
    path('', include(router.urls))
]