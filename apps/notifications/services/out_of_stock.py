from django.conf import settings
from django.core.mail import send_mail

from apps.notifications.email import build_out_of_stock_email
from apps.network.models import Outlet, Employee
from apps.catalog.models import Product


def send_out_of_stock_notification(
    dealer: Outlet, product: Product, employee: Employee
) -> None:
    subject, body = build_out_of_stock_email(dealer, product, employee)

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [employee.email],
        fail_silently=False,
    )
