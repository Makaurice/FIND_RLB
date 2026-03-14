"""Management command to compute tenant trust scores and optionally sync to Hedera."""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from tenant.trust_score import get_or_create_trust_score


class Command(BaseCommand):
    help = "Compute tenant trust scores and optionally push to Hedera."

    def add_arguments(self, parser):
        parser.add_argument(
            "--on-chain",
            action="store_true",
            help="Sync computed trust scores to Hedera via the Reputation contract.",
        )

    def handle(self, *args, **options):
        on_chain = options.get("on_chain", False)

        User = get_user_model()
        tenants = User.objects.filter(role="tenant")

        if not tenants.exists():
            self.stdout.write(self.style.WARNING("No tenants found to score."))
            return

        for user in tenants:
            score = get_or_create_trust_score(user.id, sync_on_chain=on_chain)
            self.stdout.write(
                f"{user.username} -> score {score.overall_score:.2f} (hash: {score.score_hash[:8]}...)"
            )
