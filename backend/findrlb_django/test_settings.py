from .settings import *

# Use a minimal URL conf for tests to avoid importing full project URLs
ROOT_URLCONF = 'findrlb_django.dummy_test_urls'

# Keep other settings as-is from settings.py

# Ensure project root is first on sys.path so top-level apps (e.g., `landlord`, `tenant`) are imported
import sys
import os
PROJECT_ROOT = BASE_DIR
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))
