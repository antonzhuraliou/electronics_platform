import uuid

from django.db import models
from django.core.exceptions import ValidationError

from config import settings


class Outlet(models.Model):
    """A physical trading point in the electronics network."""

    class OutletType(models.TextChoices):
        HEAD = "HEAD", "Head Office"
        DEALER = "DEALER", "Dealer Center"

    outlet_type = models.CharField(
        max_length=10,
        choices=OutletType.choices,
        verbose_name="Outlet type",
    )
    name = models.CharField(max_length=100, verbose_name="Name")

    country = models.CharField(max_length=50, verbose_name="Country")
    city = models.CharField(max_length=50, verbose_name="City")
    street = models.CharField(max_length=100, verbose_name="Street")
    house_number = models.CharField(max_length=20, verbose_name="House number")

    daily_revenue = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Daily revenue",
    )

    class Meta:
        verbose_name = "Outlet"
        verbose_name_plural = "Outlets"

        constraints = [
            models.UniqueConstraint(
                fields=["outlet_type"],
                condition=models.Q(outlet_type="HEAD"),
                name="unique_head_office"
            )
        ]

    def __str__(self) -> str:
        return f"{self.get_outlet_type_display()} — {self.name}"

    def clean(self) -> None:
        if (
            self.outlet_type == self.OutletType.HEAD
            and Outlet.objects.filter(outlet_type=self.OutletType.HEAD)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                "There must be exactly one head office in the system."
            )

    @property
    def address(self) -> str:
        return f"{self.country}, {self.city}, {self.street}, д. {self.house_number}"


class OutletAPIKey(models.Model):
    """Represents an API key used to authenticate requests for a specific outlet."""

    key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="API-key")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User", related_name="api_keys")
    outlet = models.ForeignKey('Outlet', on_delete=models.CASCADE, verbose_name="Outlet", related_name="api_keys")
    is_admin = models.BooleanField(default=False, verbose_name="Admin access")


    class Meta:
        verbose_name = "Outlet API Key"
        verbose_name_plural = "Outlet API Keys"

    def __str__(self) -> str:
        return f"Key for {self.user.username} at {self.outlet.name}"


class Employee(models.Model):
    """A staff member belonging to a specific outlet."""

    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Outlet",
    )

    full_name = models.CharField(max_length=200, verbose_name="Full name")
    phone = models.CharField(max_length=30, verbose_name="Phone number")
    email = models.EmailField(verbose_name="E-mail")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name="User",
        null=True
    )

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self) -> str:
        return f"{self.full_name} ({self.outlet.name})"
