from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Product(models.Model):
    """A product entry in the shared electronics catalogue."""

    brand = models.CharField(max_length=50, verbose_name="Brand")
    model = models.CharField(max_length=25, verbose_name="Model")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price")
    release_date = models.DateField(verbose_name="Release date")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["brand", "model"]

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"

    def clean(self) -> None:
        if self.release_date and self.release_date > timezone.now().date():
            raise ValidationError(
                {"release_date": "Release date cannot be in the future."}
            )
