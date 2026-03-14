"""Thin wrapper to expose backend service event utilities under the `service` package.

This allows other parts of the system to import `service.events` even though the
actual implementation lives under `backend.service`.
"""

from backend.service.events import log_user_event  # noqa: F401

__all__ = ["log_user_event"]
