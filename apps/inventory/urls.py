from django.urls import path
from .views import OutletsByProductView

urlpatterns = [
    path("inventory/by-product/", OutletsByProductView.as_view(), name="outlets-by-product"),
]
