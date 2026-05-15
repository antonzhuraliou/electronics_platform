import django_filters

from .models import Outlet


class OutletFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")

    class Meta:
        model = Outlet
        fields = ["city"]
