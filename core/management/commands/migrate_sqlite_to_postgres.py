import os
from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core import management
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "One-time: copy data from sqlite_old to default (Postgres) if Postgres is empty."

    def handle(self, *args, **options):
        default_conn = connections["default"]
        fixture_path = os.getenv("FIXTURE_PATH", "/app/dumpdata.json")

        default_engine = default_conn.settings_dict.get("ENGINE", "")
        if "postgresql" not in default_engine:
            self.stdout.write("Default database is not Postgres; skipping copy.")
            return

        # Check if default DB appears empty using the custom user model
        user_model = get_user_model()
        try:
            user_count = user_model.objects.using("default").count()
        except Exception:
            management.call_command("migrate", interactive=False)
            try:
                user_count = user_model.objects.using("default").count()
            except Exception:
                user_count = 0

        if user_count > 0:
            self.stdout.write(self.style.SUCCESS("Postgres already has data; skipping copy."))
            return

        # If a fixture path is provided and exists, prefer loading from it
        if fixture_path and Path(fixture_path).exists():
            self.stdout.write(f"Fixture found at {fixture_path}; loading into Postgres...")
            management.call_command("migrate", interactive=False)
            management.call_command("loaddata", fixture_path)
            self.stdout.write(self.style.SUCCESS("Fixture loaded into Postgres."))
            return

        # Ensure sqlite_old is configured before attempting a copy
        if "sqlite_old" not in connections.databases:
            self.stdout.write(self.style.WARNING("sqlite_old database alias not configured and no fixture found; skipping."))
            return

        # Dump from sqlite_old
        self.stdout.write("Dumping data from sqlite_old...")
        management.call_command(
            "dumpdata",
            database="sqlite_old",
            exclude=["contenttypes", "auth.Permission"],
            output="/tmp/sqlite_dump.json",
            natural_foreign=True,
            natural_primary=True,
        )

        # Migrate default before loading
        self.stdout.write("Applying migrations to default (Postgres)...")
        management.call_command("migrate", interactive=False)

        # Load into default
        # To avoid unique constraint conflicts (e.g., fixtures or default seeds),
        # purge existing data from non-system apps before loading.
        self.stdout.write("Clearing existing data from Postgres (non-system apps)...")
        system_apps = {"contenttypes", "auth", "admin", "sessions"}
        for app_config in list(apps.get_app_configs())[::-1]:
            if app_config.name.split(".")[-1] in system_apps:
                continue
            models_list = list(app_config.get_models())
            for model in models_list[::-1]:
                try:
                    model.objects.using("default").all().delete()
                except Exception:
                    # some tables may not exist yet; ignore
                    pass

        self.stdout.write("Loading data into Postgres...")
        management.call_command("loaddata", "/tmp/sqlite_dump.json")
        self.stdout.write(self.style.SUCCESS("Data copied from SQLite to Postgres."))
