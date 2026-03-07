"""Run periodic background tasks for FIND-RLB.

This management command is intended to be run as a long-lived process (systemd service,
Docker sidecar, or cron job that restarts it) and will periodically invoke
retraining and other maintenance tasks.

Usage:
    python backend/manage.py run_periodic_tasks --interval 86400

By default it will run the `train_recommender` command once every 24 hours.
"""

from __future__ import annotations

import time

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Run periodic tasks (e.g. train recommender) on a schedule. "
        "This command runs forever unless interrupted."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=86400,
            help="Seconds between each run of the periodic task (default: 86400 / 24h).",
        )
        parser.add_argument(
            "--once",
            action="store_true",
            help="Run the periodic tasks once then exit (useful for cron/CI).",
        )

    def handle(self, *args, **options):
        interval = options.get("interval")
        run_once = options.get("once")

        def _run_tasks():
            self.stdout.write("[PeriodicTasks] Running scheduled tasks...")

            try:
                call_command("train_recommender")
            except Exception as exc:
                self.stderr.write(f"[PeriodicTasks] Error running train_recommender: {exc}")

        # Run at least once immediately
        _run_tasks()

        if run_once:
            return

        self.stdout.write(f"[PeriodicTasks] Sleeping for {interval} seconds...")
        while True:
            time.sleep(interval)
            _run_tasks()
