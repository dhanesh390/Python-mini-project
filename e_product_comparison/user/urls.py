from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register('api/v1/user', views.UserViewSet)

urlpatterns = [
    path('api/v1/update/user/', views.UserUpdateView.as_view()),
    path('api/v1/users/', views.GetUserByRole.as_view()),
    path('', include(router.urls))
]
