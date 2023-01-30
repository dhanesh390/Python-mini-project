from django.urls import path, include
from offer import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/v1/product/offer', views.OfferViewSet)


urlpatterns = [
    path('api/v1/product/view/', views.ViewOffers.as_view()),
    path('api/v1/product/offer/update/<int:offer_id>', views.OfferUpdateViewSet.as_view()),
    path('', include(router.urls))
]
