import logging

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.network.models import Employee, Outlet
from apps.network.tasks import clear_daily_revenue_async

logger = logging.getLogger(__name__)


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0
    fields = ["full_name", "phone", "email", "user"]


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "outlet_type",
        "city",
        "country",
        "daily_revenue",
    ]
    list_filter = ["outlet_type", "city", "country"]
    search_fields = ["name", "city"]
    inlines = [EmployeeInline]
    actions = ["clear_daily_revenue"]

    @admin.action(description="Clear daily revenue for selected outlets")
    def clear_daily_revenue(self, request: HttpRequest, queryset: QuerySet) -> None:
        ids = list(queryset.values_list("id", flat=True))
        if len(ids) > 5:
            clear_daily_revenue_async.delay(ids)
            logger.info(
                "Admin '%s' triggered async clear_daily_revenue for %d outlets: %s",
                request.user,
                len(ids),
                ids,
            )
            self.message_user(
                request,
                f"Daily revenue cleanup for {len(ids)} outlets started asynchronously.",
                messages.SUCCESS,
            )
        else:
            queryset.update(daily_revenue=0)
            logger.info(
                "Admin '%s' cleared daily_revenue for %d outlets: %s",
                request.user,
                len(ids),
                ids,
            )
            self.message_user(
                request,
                f"Daily revenue cleared for {len(ids)} outlets.",
                messages.SUCCESS,
            )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "outlet", "phone", "email"]
    list_filter = ["outlet"]
    search_fields = ["full_name", "email"]
    autocomplete_fields = ["outlet"]
