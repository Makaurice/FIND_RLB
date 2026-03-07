"""Simple property recommender utilities for FIND-RLB.

This module is intentionally lightweight and designed to be a starting point.
It can be extended with real user interaction logging and more advanced
modeling (collaborative filtering, content-based filtering, deep learning, etc.).

To train a basic model, collect a dataset of property features (price, bedrooms,
bathrooms, square footage, etc.) and optionally user preferences.
"""

from __future__ import annotations

import json
import os
import time
from typing import Dict, Iterable, List, Optional, Tuple

import joblib
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DEFAULT_MODEL_PATH = os.getenv('RECOMMENDER_MODEL_PATH', 'data_science/recommender.joblib')


def _features_from_property(property_data: Dict) -> List[float]:
    """Extract a numeric feature vector from a property record.

    This should be adjusted to match your actual property schema.
    """
    # Common property fields that can be used for simple similarity
    price = float(property_data.get('price', 0) or 0)
    bedrooms = float(property_data.get('bedrooms', 0) or 0)
    bathrooms = float(property_data.get('bathrooms', 0) or 0)
    sqft = float(property_data.get('sqft', 0) or 0)

    # Optional: include location (lat/lng) if available
    lat = float(property_data.get('latitude', 0) or 0)
    lng = float(property_data.get('longitude', 0) or 0)

    return [price, bedrooms, bathrooms, sqft, lat, lng]


class PropertyRecommender:
    """A simple property recommender using nearest neighbors."""

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.pipeline: Optional[Pipeline] = None
        self.property_ids: List[str] = []
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.model_path):
            payload = joblib.load(self.model_path)
            self.pipeline = payload.get('pipeline')
            self.property_ids = payload.get('property_ids', [])

    def save(self) -> None:
        if not self.pipeline:
            raise RuntimeError('No trained model to save')
        os.makedirs(os.path.dirname(self.model_path) or '.', exist_ok=True)
        joblib.dump({'pipeline': self.pipeline, 'property_ids': self.property_ids}, self.model_path)

    def fit(self, properties: Iterable[Dict], n_neighbors: int = 5) -> Dict[str, float]:
        """Train the recommender from a list of property dictionaries.

        Returns a dict with training metadata (number of properties and duration in seconds).
        """
        feature_matrix = []
        ids = []

        for p in properties:
            features = _features_from_property(p)
            feature_matrix.append(features)
            # Keep a stable ID so we can map neighbors back to records
            ids.append(str(p.get('id') or p.get('property_id') or len(ids)))

        if not feature_matrix:
            raise ValueError('No property data provided to train recommender')

        n_properties = len(feature_matrix)
        X = np.array(feature_matrix, dtype=float)

        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto')),
        ])

        start_time = time.perf_counter()
        self.pipeline.fit(X)
        duration_seconds = time.perf_counter() - start_time

        self.property_ids = ids
        self.save()

        return {
            'n_properties': n_properties,
            'duration_seconds': duration_seconds,
        }

    def _build_query_vector(self, user_profile: Dict) -> np.ndarray:
        # Map user preferences into the same feature space used for properties.
        # For now, we use the same feature extraction as properties.
        return np.array([_features_from_property(user_profile)], dtype=float)

    def recommend(self, user_profile: Dict, properties: List[Dict], k: int = 3) -> List[Dict]:
        """Recommend up to `k` properties based on the user profile.

        If the internal model is not trained/loaded, falls back to a simple price-based heuristic.
        """
        if not properties:
            return []

        if self.pipeline is None:
            # Fallback: return the lowest-price properties
            return sorted(properties, key=lambda p: p.get('price', float('inf')))[:k]

        query = self._build_query_vector(user_profile)
        distances, indices = self.pipeline.named_steps['knn'].kneighbors(query, n_neighbors=min(k, len(properties)))
        indices = indices.flatten().tolist()

        # Ensure we map back to the provided properties list; if the training set differs,
        # fall back to a simple ordering.
        try:
            return [properties[i] for i in indices]
        except Exception:
            return sorted(properties, key=lambda p: p.get('price', float('inf')))[:k]


def load_sample_properties() -> List[Dict]:
    """Loads sample properties from a JSON fixture (for quick testing)."""
    sample_path = os.path.join(os.path.dirname(__file__), 'sample_properties.json')
    if not os.path.exists(sample_path):
        return []
    with open(sample_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main() -> None:
    """Simple CLI entrypoint for quickly training a new recommender."""
    properties = load_sample_properties()
    if not properties:
        raise SystemExit('No sample properties available; add data_science/sample_properties.json')

    recommender = PropertyRecommender()
    train_info = recommender.fit(properties)
    duration = train_info.get('duration_seconds')
    n_properties = train_info.get('n_properties', len(properties))
    print(
        f'Trained recommender with {n_properties} properties (took {duration:.2f}s) and wrote model to {recommender.model_path}'
    )


if __name__ == '__main__':
    main()
