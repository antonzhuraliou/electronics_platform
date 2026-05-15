import logging
import random

from celery import shared_task
from django.db import transaction
from django.db.models import F

from apps.inventory.models import StockItem
from apps.inventory.services.stock_simulation import (
    choose_random_dealer,
    get_available_stock_for_update,
    simulate_sales,
)
from apps.network.models import Outlet
from apps.network.tasks import send_out_of_stock_email

logger = logging.getLogger(__name__)


@shared_task
def restock_zero_items() -> int:
    """For stock items in dealer centers with zero quantity,
    increase the quantity by a random integer from 5 to 25 units.
    """

    from apps.inventory.models import StockItem

    zero_items = list(StockItem.objects.filter(quantity=0))

    for item in zero_items:
        item.quantity = random.randint(5, 25)

    StockItem.objects.bulk_update(zero_items, ["quantity"])
    logger.info("Restocked %d zero-stock items.", len(zero_items))
    return len(zero_items)


@shared_task
def hourly_sales_simulation() -> int:
    """Select several random items from a random dealer center;
    reduce quantity by 1–10 for each item;
    add the reduction amount to the dealer's daily revenue.
    """

    dealer = choose_random_dealer()
    if not dealer:
        return 0

    with transaction.atomic():
        stock_items = get_available_stock_for_update(dealer)

        if not stock_items:
            return 0

        sample_size = random.randint(1, min(5, len(stock_items)))
        selected = random.sample(stock_items, sample_size)

        total_revenue, out_of_stock_items = simulate_sales(selected)

        StockItem.objects.bulk_update(selected, ["quantity"])

        Outlet.objects.filter(id=dealer.id).update(
            daily_revenue=F("daily_revenue") + total_revenue
        )

        logger.info(
            "Simulated sales at '%s': revenue +%s, %d items went to zero.",
            dealer.name,
            total_revenue,
            len(out_of_stock_items),
        )

    if out_of_stock_items:
        for item in out_of_stock_items:
            send_out_of_stock_email.delay(dealer.id, item.product_id)

    return len(out_of_stock_items)
