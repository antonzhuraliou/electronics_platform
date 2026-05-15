import logging

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from apps.network.models import Outlet
from apps.network.serializers import OutletSerializer
from .filters import OutletFilter
from .parameters import PRODUCT_ID_PARAM

logger = logging.getLogger(__name__)


@extend_schema(parameters=[PRODUCT_ID_PARAM])
class OutletsByProductView(generics.ListAPIView):
    """List outlets that have stock for a specific product."""

    serializer_class = OutletSerializer
    filterset_class = OutletFilter

    def get_queryset(self):
        product_id = self.request.query_params.get("product_id")

        if not product_id:
            raise ValidationError({"product_id": "Parameter product_id is required."})

        qs = Outlet.objects.prefetch_related("employees")
        filtered_qs = self.filter_queryset(qs)
        logger.debug(
            "by-product query: product_id=%s found %d outlets with stock, user='%s'",
            product_id, filtered_qs.count(), self.request.user,
        )
        return filtered_qs
