"""Thin wrapper to expose backend blockchain utilities under the `service` package.

This allows other parts of the system to import `service.blockchain_service` even
though the implementation lives in `backend.blockchain_service`.
"""

from backend.blockchain_service import BlockchainService  # noqa: F401

__all__ = ["BlockchainService"]
