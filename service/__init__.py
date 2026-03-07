"""Service app package for Django.

This package is a thin wrapper around the backend/service module, allowing the
Django project to treat it as a first-class app named 'service'.
"""

# Expose the backend implementation for easier imports.
from backend.service import *  # noqa: F401,F403
