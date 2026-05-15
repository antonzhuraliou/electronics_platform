import random

from apps.inventory.models import StockItem
from apps.network.models import Outlet


def choose_random_dealer() -> Outlet | None:
    dealers = list(Outlet.objects.filter(outlet_type=Outlet.OutletType.DEALER))
    return random.choice(dealers) if dealers else None


def get_available_stock_for_update(dealer: Outlet) -> list[StockItem]:
    return list(
        StockItem.objects.select_for_update()
        .filter(outlet=dealer, quantity__gt=0)
        .select_related("product")
    )


def simulate_sales(selected_items: list[StockItem]) -> tuple[float, list[StockItem]]:
    total_revenue = 0
    out_of_stock_items = []

    for item in selected_items:
        reduction = random.randint(1, min(10, item.quantity))
        item.quantity -= reduction
        total_revenue += reduction * item.product.price

        if item.quantity == 0:
            out_of_stock_items.append(item)

    return total_revenue, out_of_stock_items
