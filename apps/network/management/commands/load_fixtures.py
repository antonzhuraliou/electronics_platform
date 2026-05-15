import json
import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from apps.network.models import Outlet
from config import settings
from config.celery_schedule import SCHEDULES

logger = logging.getLogger(__name__)

FIXTURES_DIR = settings.BASE_DIR / "fixtures"

FIXTURE_ORDER = [
    "users.json",
    "outlets.json",
    "employees.json",
    "products.json",
    "stock.json",
    "outlet_api_keys.json",
]


class Command(BaseCommand):
    help = "Load test data from JSON fixtures"

    def handle(self, *args, **options):

        if Outlet.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Database is already populated. Skipping load_fixtures."
                )
            )
            logger.info("load_fixtures skipped: database already contains data.")
            return

        logger.info("load_fixtures started.")
        for filename in FIXTURE_ORDER:
            path = FIXTURES_DIR / filename

            if not path.exists():
                self.stdout.write(self.style.ERROR(f"File not found: {path}"))
                logger.error("Fixture file not found: %s", path)
                return

            self.stdout.write(f"  Loading {filename}...")
            call_command("loaddata", str(path), verbosity=0)
            logger.info("Loaded fixture: %s", filename)

        logger.info("load_fixtures completed.")
        self.setup_schedules()

        self.stdout.write(self.style.SUCCESS("\n✓ Fixtures loaded!"))
        self.stdout.write("Superuser: username=head_director  password=admin1234")

    def setup_schedules(self):
        for item in SCHEDULES:
            schedule = self._get_or_create_schedule(item["cron"])

            PeriodicTask.objects.update_or_create(
                name=item["name"],
                defaults={
                    "crontab": schedule,
                    "task": item["task"],
                    "args": json.dumps([]),
                    "enabled": True,
                },
            )
        self.stdout.write(
            self.style.SUCCESS("Celery Beat schedules have been configured.")
        )

    def _get_or_create_schedule(self, cron: dict):
        return CrontabSchedule.objects.get_or_create(**cron)[0]
