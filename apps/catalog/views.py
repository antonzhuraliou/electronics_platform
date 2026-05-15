import logging

from rest_framework import viewsets

from .models import Product
from apps.catalog.serializers import ProductSerializer

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product CRUD operations."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer) -> None:
        instance = serializer.save()
        logger.info(
            "Product created: id=%d '%s %s' price=%s by user='%s'",
            instance.pk, instance.brand, instance.model,
            instance.price, self.request.user,
        )

    def perform_update(self, serializer) -> None:
        instance = serializer.save()
        logger.info(
            "Product updated: id=%d '%s %s' by user='%s'",
            instance.pk, instance.brand, instance.model, self.request.user,
        )

    def perform_destroy(self, instance: Product) -> None:
        logger.info(
            "Product deleted: id=%d '%s %s' by user='%s'",
            instance.pk, instance.brand, instance.model, self.request.user,
        )
        instance.delete()