from django.contrib import admin

from apps.catalog.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["brand", "model", "price", "release_date"]
    list_filter = ["brand"]
    search_fields = ["brand", "model"]
    ordering = ["brand", "model"]
