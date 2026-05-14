from django.db import models

from apps.catalog.models import Product
from apps.network.models import Outlet


class StockItem(models.Model):
    """ A stock entry linking a dealer outlet to a catalogue product."""

    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE,
        related_name="stock_items",
        limit_choices_to={"outlet_type": Outlet.OutletType.DEALER},
        verbose_name="Dealer center",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_items",
        verbose_name="Product",
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")

    class Meta:
        verbose_name = "Stock item"
        verbose_name_plural = "Stock items"
        unique_together = [("outlet", "product")]

    def __str__(self):
        return f"{self.product} @ {self.outlet.name} — {self.quantity} in stock"
