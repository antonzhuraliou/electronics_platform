import logging
from celery import shared_task

from apps.catalog.models import Product
from apps.network.models import Outlet
from apps.notifications.services.out_of_stock import send_out_of_stock_notification

logger = logging.getLogger(__name__)


@shared_task
def clear_daily_revenue_async(outlet_ids: list[int]) -> int:
    from apps.network.models import Outlet

    updated = Outlet.objects.filter(id__in=outlet_ids).update(daily_revenue=0)
    logger.info("Cleared daily_revenue for %d outlets (async).", updated)
    return updated


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_out_of_stock_email(self, dealer_id: int, product_id: int) -> None:
    """Send an email to the head office employee about product out of stock."""

    dealer = Outlet.objects.filter(pk=dealer_id).only("id", "name", "address").first()

    if not dealer:
        return

    product = Product.objects.filter(pk=product_id).only("id", "brand", "model").first()
    if not product:
        return

    head = (
        Outlet.objects.filter(outlet_type=Outlet.OutletType.HEAD)
        .prefetch_related("employees")
        .first()
    )
    if not head:
        return

    employee = head.employees.first()
    if not employee or not employee.email:
        return

    send_out_of_stock_notification(dealer, product, employee)

    logger.info(
        "Sent out-of-stock email to %s for product %s at dealer %s.",
        employee.email,
        product,
        dealer.name,
    )


@shared_task
def reset_daily_revenue() -> int:
    from apps.network.models import Outlet

    updated = Outlet.objects.filter(outlet_type=Outlet.OutletType.DEALER).update(
        daily_revenue=0
    )
    logger.info("Reset daily_revenue for %d dealers.", updated)
    return updated
