"""Django management command to train the property recommender model."""

from __future__ import annotations

from typing import List

from django.core.management.base import BaseCommand

from data_science.recommender import PropertyRecommender
from property.models import Property


class Command(BaseCommand):
    help = "Train the property recommender model from the current property catalog."

    def add_arguments(self, parser):
        parser.add_argument(
            "--k",
            type=int,
            default=5,
            help="Number of nearest neighbors to train the recommender with.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run the command without writing the model file (useful for preview).",
        )

    def handle(self, *args, **options):
        k = options.get("k", 5)
        dry_run = options.get("dry_run", False)

        self.stdout.write("Collecting properties to train recommender...")

        properties: List[dict] = list(
            Property.objects.values(
                'id',
                'price',
                'beds',
                'location',
                'property_type',
                'lat',
                'lon',
            )
        )

        if not properties:
            self.stderr.write("No properties found, cannot train recommender.")
            return

        self.stdout.write(f"Training recommender on {len(properties)} properties (k={k})...")
        recommender = PropertyRecommender()
        train_info = recommender.fit(properties, n_neighbors=k)

        duration = train_info.get('duration_seconds')
        n_properties = train_info.get('n_properties', len(properties))

        if dry_run:
            self.stdout.write(
                f"Dry run: model training completed on {n_properties} properties (took {duration:.2f}s) but not saved."
            )
        else:
            self.stdout.write(
                f"Recommender trained on {n_properties} properties (took {duration:.2f}s) and saved to {recommender.model_path}"
            )
