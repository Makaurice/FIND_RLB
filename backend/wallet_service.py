"""
Wallet Management System
Manages user wallets:
- Hedera native wallets
- Internal FIND token walances
- Escrow/savings accounts
- Payment authorization
"""

from typing import Optional, Dict, Any
from datetime import datetime
from hedera_integration import HederaClient

class WalletService:
    """Manages user wallets and funds."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.hedera_account: Optional[str] = None
        self.internal_balances = {
            'find_token': 0.0,
            'escrow_account': 0.0,
            'savings_vault': 0.0,
            'reputation_bonus': 0.0,
        }
        self.transaction_log = []
        self.connected_banks = []

    def create_custodial_wallet(self) -> Dict[str, Any]:
        """
        Create a custodial wallet (FIND-RLB hosted).
        User doesn't own private key; FIND-RLB manages it.
        """
        return {
            'userId': self.user_id,
            'walletType': 'CUSTODIAL',
            'hedera_account': f'0.0.{hash(self.user_id) % 1000000}',
            'status': 'ACTIVE',
            'createdAt': datetime.now().isoformat(),
            'security': 'TWO_FACTOR_AUTH',
        }

    def create_non_custodial_wallet(self) -> Dict[str, Any]:
        """
        Create non-custodial wallet (user owns private key).
        User can export and use with other Hedera wallets.
        """
        return {
            'userId': self.user_id,
            'walletType': 'NON_CUSTODIAL',
            'message': 'User must securely store private key',
            'generatedPrivateKey': '0x' + 'a' * 64,  # Placeholder
            'publicKey': '0x' + 'b' * 128,
            'hedera_account': '0.0.123456',
            'createdAt': datetime.now().isoformat(),
            'warning': 'Lost keys = lost funds. NEVER share private key.',
        }

    def link_bank_account(self, bank_name: str, account_number: str) -> Dict[str, Any]:
        """
        Link a bank account for deposits/withdrawals (M-Pesa, etc.).
        In production: KYC verification required.
        """
        return {
            'userId': self.user_id,
            'bank': bank_name,
            'accountNumber': account_number[-4:] + '****',  # Masked
            'status': 'VERIFIED',
            'linkedAt': datetime.now().isoformat(),
            'dailyLimit': 1000.0,  # USD
            'monthlyLimit': 20000.0,
        }

    def get_balance(self, account_type: str = 'all') -> Dict[str, Any]:
        """Get wallet balance(s)."""
        if account_type == 'all':
            return {
                'userId': self.user_id,
                'balances': self.internal_balances,
                'totalValue': sum(self.internal_balances.values()),
                'lastUpdated': datetime.now().isoformat(),
            }
        return {
            'userId': self.user_id,
            'accountType': account_type,
            'balance': self.internal_balances.get(account_type, 0.0),
        }

    def deposit_from_bank(self, amount: float, bank: str) -> Dict[str, Any]:
        """Deposit fiat currency from linked bank account."""
        self.internal_balances['find_token'] += amount
        
        transaction = {
            'type': 'DEPOSIT',
            'from': bank,
            'amount': amount,
            'to_account': 'find_token',
            'status': 'CONFIRMED',
            'timestamp': datetime.now().isoformat(),
            'transactionId': '0x' + 'c' * 64,
        }
        self.transaction_log.append(transaction)
        return transaction

    def withdraw_to_bank(self, amount: float, bank: str) -> Dict[str, Any]:
        """Withdraw to linked bank account."""
        if self.internal_balances['find_token'] < amount:
            return {'error': 'Insufficient balance'}
        
        self.internal_balances['find_token'] -= amount
        
        transaction = {
            'type': 'WITHDRAWAL',
            'from': 'find_token',
            'to': bank,
            'amount': amount,
            'status': 'PROCESSING',
            'estimatedDelivery': '1-2 business days',
            'transactionId': '0x' + 'd' * 64,
            'timestamp': datetime.now().isoformat(),
        }
        self.transaction_log.append(transaction)
        return transaction

    def transfer_to_user(self, recipient_id: str, amount: float, reason: str) -> Dict[str, Any]:
        """
        Transfer FIND tokens to another user.
        On-chain transaction via Hedera.
        """
        if self.internal_balances['find_token'] < amount:
            return {'error': 'Insufficient balance'}
        
        self.internal_balances['find_token'] -= amount
        
        transaction = {
            'type': 'TRANSFER',
            'from': self.user_id,
            'to': recipient_id,
            'amount': amount,
            'reason': reason,
            'status': 'CONFIRMED',
            'transactionHash': '0x' + 'e' * 64,
            'timestamp': datetime.now().isoformat(),
        }
        self.transaction_log.append(transaction)
        return transaction

    def lock_funds_escrow(self, amount: float, for_lease_id: int) -> Dict[str, Any]:
        """Lock funds in escrow for lease-related purposes."""
        if self.internal_balances['find_token'] < amount:
            return {'error': 'Insufficient balance'}
        
        self.internal_balances['find_token'] -= amount
        self.internal_balances['escrow_account'] += amount
        
        return {
            'userId': self.user_id,
            'amount': amount,
            'leaseId': for_lease_id,
            'status': 'LOCKED_IN_ESCROW',
            'lockedAt': datetime.now().isoformat(),
            'releaseTrigger': 'End of lease or dispute resolution',
        }

    def release_escrow_funds(self, lease_id: int, amount: float) -> Dict[str, Any]:
        """Release escrow funds (after lease completion or dispute)."""
        if self.internal_balances['escrow_account'] < amount:
            return {'error': 'Insufficient escrow balance'}
        
        self.internal_balances['escrow_account'] -= amount
        self.internal_balances['find_token'] += amount
        
        return {
            'userId': self.user_id,
            'amount': amount,
            'leaseId': lease_id,
            'status': 'RELEASED',
            'releasedAt': datetime.now().isoformat(),
        }

    def deposit_savings(self, amount: float, plan_id: int) -> Dict[str, Any]:
        """Deposit into savings-to-own plan."""
        transaction = {
            'userId': self.user_id,
            'type': 'SAVINGS_DEPOSIT',
            'amount': amount,
            'planId': plan_id,
            'newSavingsBalance': self.internal_balances['savings_vault'] + amount,
            'status': 'CONFIRMED',
            'timestamp': datetime.now().isoformat(),
        }
        
        self.internal_balances['savings_vault'] += amount
        self.transaction_log.append(transaction)
        return transaction

    def claim_reputation_bonus(self, amount: float, for_action: str) -> Dict[str, Any]:
        """Claim FIND tokens as reputation bonus (referral, review, etc.)."""
        self.internal_balances['reputation_bonus'] += amount
        
        return {
            'userId': self.user_id,
            'amount': amount,
            'reason': for_action,
            'newBalance': self.internal_balances['reputation_bonus'],
            'status': 'CLAIMED',
            'claimedAt': datetime.now().isoformat(),
        }

    def get_transaction_history(self, limit: int = 50) -> Dict[str, Any]:
        """Get transaction history."""
        return {
            'userId': self.user_id,
            'transactionCount': len(self.transaction_log),
            'transactions': self.transaction_log[-limit:],
        }

    def authorize_payment(self, lease_id: int, amount: float, max_auto_debit: float = 0) -> Dict[str, Any]:
        """
        Authorize automatic rent payment.
        If max_auto_debit > 0, system can auto-debit up to that amount.
        """
        return {
            'userId': self.user_id,
            'leaseId': lease_id,
            'authorizedAmount': amount,
            'autoDebitMax': max_auto_debit,
            'status': 'AUTHORIZED',
            'validFrom': datetime.now().isoformat(),
            'validUntil': 'Never (until revoked)',
        }

    def revoke_payment_authorization(self, lease_id: int) -> Dict[str, Any]:
        """Revoke payment authorization."""
        return {
            'userId': self.user_id,
            'leaseId': lease_id,
            'status': 'REVOKED',
            'revokedAt': datetime.now().isoformat(),
        }
