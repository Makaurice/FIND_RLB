"""
Hedera Integration Module
Provides interfaces for:
- Smart Contract interactions (HCS)
- Token Service (HTS)
- Payments and transactions
- Identity and verification
"""

from typing import Optional, Dict, Any
from datetime import datetime

class HederaClient:
    """Compatibility wrapper for the real HederaClient implementation.

    The previous version of this file contained stubbed placeholder logic that
    simulated Hedera operations.  We now maintain the legacy import path but
    delegate all work to ``hedera_integration_v2.HederaClient`` which contains a
    full production implementation.
    """

    def __init__(self, account_id: str, private_key: str, network: str = "testnet"):
        # Create the underlying real client and store values for backwards
        # compatibility.  Any missing attributes or methods will be forwarded via
        # ``__getattr__`` below.
        from .hedera_integration_v2 import HederaClient as RealClient

        self._real = RealClient(account_id, private_key, network)
        self.account_id = account_id
        self.network = network
        self.transaction_history = self._real.transaction_history

    # delegate all methods to real implementation
    def __getattr__(self, name):
        return getattr(self._real, name)

    def create_token(self, name: str, symbol: str, decimals: int = 18) -> Dict[str, Any]:
        """Delegate to underlying Hedera client."""
        return self._real.create_token(name, symbol, decimals)

    def deploy_contract(self, bytecode: str, abi: list) -> Dict[str, Any]:
        """Delegate to underlying Hedera client."""
        return self._real.deploy_contract(bytecode, abi)

    def call_contract(self, contract_id: str, function: str, params: list, gas: int = 100000) -> Dict[str, Any]:
        """Delegate to underlying Hedera client."""
        return self._real.call_contract(contract_id, function, params, gas)

    def associate_token(self, token_id: str, account_id: Optional[str] = None) -> Dict[str, Any]:
        return self._real.associate_token(token_id, account_id)

    def transfer_token(self, token_id: str, from_account: str, to_account: str, amount: int) -> Dict[str, Any]:
        return self._real.transfer_token(token_id, from_account, to_account, amount)

    def get_balance(self, account_id: Optional[str] = None) -> Dict[str, Any]:
        return self._real.get_balance(account_id)

    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        return self._real.get_transaction_status(transaction_id)

    def get_contract_state(self, contract_id: str) -> Dict[str, Any]:
        return self._real.get_contract_state(contract_id)
