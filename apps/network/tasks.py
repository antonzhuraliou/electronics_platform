import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def clear_daily_revenue_async(outlet_ids: list[int]):
    from apps.network.models import Outlet

    updated = Outlet.objects.filter(id__in=outlet_ids).update(daily_revenue=0)
    logger.info("Cleared daily_revenue for %d outlets (async).", updated)
    return updated
