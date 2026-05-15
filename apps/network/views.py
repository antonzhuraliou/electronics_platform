import logging

from django.db.models import Avg, QuerySet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .filters import OutletFilter
from .models import Outlet
from .serializers import (
    OutletSerializer,
    OutletAboveAverageSerializer,
)

logger = logging.getLogger(__name__)


class OutletViewSet(
    viewsets.ModelViewSet
):
    """ViewSet for Outlet CRUD and custom statistics actions."""

    serializer_class = OutletSerializer
    filterset_class = OutletFilter

    def get_queryset(self) -> QuerySet[Outlet]:
        qs = Outlet.objects.prefetch_related("employees").order_by("id")

        user = self.request.user
        outlet_key_outlet = getattr(user, "_outlet_api_key_outlet", None)
        is_api_key_admin = getattr(user, "_outlet_api_key_is_admin", False)

        if is_api_key_admin:
            return qs

        if outlet_key_outlet is not None:
            return qs.filter(pk=outlet_key_outlet.pk)

        return qs

    def perform_create(self, serializer) -> None:
        instance = serializer.save()
        logger.info(
            "Outlet created: id=%d name='%s' type=%s by user='%s'",
            instance.pk, instance.name, instance.outlet_type, self.request.user,
        )

    def perform_update(self, serializer) -> None:
        instance = serializer.save()
        logger.info(
            "Outlet updated: id=%d name='%s' by user='%s'",
            instance.pk, instance.name, self.request.user,
        )

    def perform_destroy(self, instance) -> None:
        if instance.outlet_type == Outlet.OutletType.HEAD:
            from rest_framework.exceptions import PermissionDenied

            logger.warning(
                "Attempt to delete HEAD outlet id=%d by user='%s' — denied.",
                instance.pk, self.request.user,
            )
            raise PermissionDenied("You cannot delete the head office.")

        logger.info(
            "Outlet deleted: id=%d name='%s' by user='%s'",
            instance.pk, instance.name, self.request.user,
        )
        instance.delete()

    @action(detail=False, methods=["get"], url_path="above-average")
    def above_average(self, request: Request) -> Response:
        """ Outlets with revenue above the average revenue of all outlets."""
        avg = (
            Outlet.objects.filter(outlet_type=Outlet.OutletType.DEALER)
            .aggregate(avg=Avg("daily_revenue"))["avg"]
            or 0
        )
        qs = Outlet.objects.filter(
            outlet_type=Outlet.OutletType.DEALER,
            daily_revenue__gt=avg,
        ).order_by("-daily_revenue")
        logger.debug(
            "above-average query: avg=%.2f, requested_by='%s'",
            avg, request.user,
        )
        serializer = OutletAboveAverageSerializer(qs, many=True)
        return Response({"average_daily_revenue": avg, "results": serializer.data})