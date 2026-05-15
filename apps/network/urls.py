from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OutletViewSet

router = DefaultRouter()
router.register("outlets", OutletViewSet, basename="outlet")

urlpatterns = [
    path("", include(router.urls)),
]
