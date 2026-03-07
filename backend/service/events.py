"""Utilities for logging user events used by analytics and recommendation systems."""

from __future__ import annotations

from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model

from service.models import UserEvent
from property.models import Property


def log_user_event(
    user: Optional[Any],
    event_type: str,
    property_id: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> UserEvent:
    """Persist a user event for analytics and personalization."""

    user_obj = None
    if user is not None:
        User = get_user_model()
        if isinstance(user, User):
            user_obj = user
        else:
            user_obj = User.objects.filter(pk=user).first()

    property_obj = None
    if property_id is not None:
        property_obj = Property.objects.filter(pk=property_id).first()

    return UserEvent.objects.create(
        user=user_obj,
        event_type=event_type,
        property=property_obj,
        metadata=metadata or {},
    )
