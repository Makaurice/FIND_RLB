"""Build a user preference profile from stored user event logs.

This module reads `UserEvent` records from the database and aggregates them
into a simple preference vector that can be used by the recommendation system.

The design is intentionally lightweight and meant as a starting point. In a
production system you would likely use richer event schemas and more advanced
feature extraction.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Optional


def build_user_profile(user_or_id: Any, limit: int = 200) -> Dict[str, Any]:
    """Build a lightweight preference profile from recent user events.

    Args:
        user_or_id: A Django user instance or a primary key value.
        limit: Maximum number of events to consider.

    Returns:
        A dictionary of inferred preferences (price range, bed count, property type, etc.).
    """
    # Avoid importing Django models at import-time so this module can be used
    # in non-Django contexts (e.g., unit tests) without triggering settings errors.
    try:
        from django.contrib.auth import get_user_model
        from service.models import UserEvent
    except Exception:
        return {}

    User = get_user_model()
    user = None
    if isinstance(user_or_id, User):
        user = user_or_id
    else:
        try:
            user = User.objects.filter(pk=user_or_id).first()
        except Exception:
            user = None

    if user is None:
        return {}

    events = (
        UserEvent.objects.filter(user=user)
        .order_by('-created_at')
        .only('event_type', 'metadata')
        [:limit]
    )

    # Aggregate basic preferences
    prices = []
    beds = []
    property_types = Counter()

    for ev in events:
        meta = ev.metadata or {}
        if ev.event_type == 'property_search':
            if meta.get('price_min') is not None:
                prices.append(meta.get('price_min'))
            if meta.get('price_max') is not None:
                prices.append(meta.get('price_max'))
            if meta.get('beds') is not None:
                beds.append(meta.get('beds'))
            if meta.get('property_type'):
                property_types[meta.get('property_type')] += 1
        elif ev.event_type == 'view_property':
            if meta.get('price') is not None:
                prices.append(meta.get('price'))
            if meta.get('beds') is not None:
                beds.append(meta.get('beds'))
            if meta.get('property_type'):
                property_types[meta.get('property_type')] += 1

    profile: Dict[str, Any] = {}
    if prices:
        profile['price'] = sum(prices) / len(prices)
        profile['price_min'] = min(prices)
        profile['price_max'] = max(prices)
    if beds:
        profile['beds'] = int(sum(beds) / len(beds))
    if property_types:
        profile['property_type'] = property_types.most_common(1)[0][0]

    return profile
