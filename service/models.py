"""Django models for the `service` app.

This module delegates implementation to `backend.service.models` while exposing
it under the `service` package so Django can load it correctly.
"""

from backend.service.models import UserEvent  # noqa: F401

__all__ = ['UserEvent']
