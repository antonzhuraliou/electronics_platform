import django_filters
from django.db.models import QuerySet

from apps.network.models import Outlet


class OutletFilter(django_filters.FilterSet):
    """FilterSet for Outlet model with custom product filtering."""

    product_id = django_filters.NumberFilter(method="filter_by_product")

    class Meta:
        model = Outlet
        fields = ["product_id"]

    def filter_by_product(
        self, queryset: QuerySet[Outlet], name: str, value: int
    ) -> QuerySet[Outlet]:
        """Filter outlets that have stock for the given product_id."""
        from .models import StockItem

        outlet_ids = StockItem.objects.filter(
            product_id=value, quantity__gt=0
        ).values_list("outlet_id", flat=True)
        return queryset.filter(id__in=outlet_ids)
