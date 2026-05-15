from apps.network.models import Outlet, Employee
from apps.catalog.models import Product


def build_out_of_stock_email(
    dealer: Outlet, product: Product, employee: Employee
) -> tuple[str, str]:
    subject = f"⚠ Product out of stock at dealer: {dealer.name}"

    body = (
        f"Hello, {employee.full_name}!\n\n"
        f"Product out of stock at dealer center '{dealer.name}':\n"
        f"  Brand and model: {product.brand} {product.model}\n"
        f"  Dealer address: {dealer.address}\n\n"
        f"Please take steps to replenish the stock.\n"
    )

    return subject, body
