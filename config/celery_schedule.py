SCHEDULES = [
    {
        "name": "restock-zero-items",
        "cron": {
            "minute": "0",
            "hour": "9",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
        },
        "task": "apps.inventory.tasks.restock_zero_items",
    },
    {
        "name": "hourly-sales-simulation",
        "cron": {
            "minute": "0",
            "hour": "*",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
        },
        "task": "apps.inventory.tasks.hourly_sales_simulation",
    },
    {
        "name": "reset-daily-revenue",
        "cron": {
            "minute": "15",
            "hour": "21",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
        },
        "task": "apps.network.tasks.reset_daily_revenue",
    },
]
