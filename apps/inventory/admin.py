from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import QuerySet
from apps.inventory.models import StockItem


class InStockFilter(admin.SimpleListFilter):
    title = "Availability"
    parameter_name = "in_stock"

    def lookups(self, request: HttpRequest, model_admin: ModelAdmin) -> list[tuple[str, str]]:
        return [
            ("yes", "In stock"),
            ("no", "Out of stock"),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() == "yes":
            return queryset.filter(quantity__gt=0)
        if self.value() == "no":
            return queryset.filter(quantity=0)
        return queryset


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = [
        "product_link",
        "outlet_link",
        "quantity",
    ]
    list_filter = [InStockFilter, "outlet"]
    search_fields = ["product__brand", "product__model", "outlet__name"]

    def product_link(self, obj: StockItem) -> str:
        url = reverse("admin:catalog_product_change", args=[obj.product_id])
        return format_html('<a href="{}">{}</a>', url, obj.product)

    product_link.short_description = "Product"
    product_link.admin_order_field = "product__brand"

    def outlet_link(self, obj: StockItem) -> str:
        url = reverse("admin:network_outlet_change", args=[obj.outlet_id])
        return format_html('<a href="{}">{}</a>', url, obj.outlet.name)

    outlet_link.short_description = "Dealer Center"
    outlet_link.admin_order_field = "outlet__name"
