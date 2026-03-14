"""
Hedera Blockchain Integration for FIND-RLB AI Agents
Provides blockchain utilities for all AI agents to interact with smart contracts
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

try:
    from backend.hedera_contract_executor import HederaContractExecutor
    from hedera import ContractFunctionParameters, Hbar, HbarUnit
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    BLOCKCHAIN_AVAILABLE = False


class BlockchainService:
    """Centralized blockchain operations for AI agents"""
    
    def __init__(self):
        """Initialize blockchain service"""
        load_dotenv()
        self.executor = HederaContractExecutor() if BLOCKCHAIN_AVAILABLE else None
        self.is_available = self.executor is not None and self.executor.client is not None
    
    # ========== RENT ESCROW OPERATIONS ==========
    
    def deposit_rent_payment(self, tenant_id: str, amount: float) -> bool:
        """
        Tenant deposits rent payment to escrow contract
        
        Args:
            tenant_id: Hedera account ID or address
            amount: Rent amount in HBAR
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available:
            print("❌ Blockchain service not available")
            return False
        
        try:
            contract_id = os.getenv('HEDERA_RENTESCROW_CONTRACT_ID')
            if not contract_id:
                print("❌ RentEscrow contract not configured")
                return False
            
            params = ContractFunctionParameters()
            params.add_string(tenant_id)
            params.add_uint256(int(amount * 10**8))
            
            return self.executor.execute_payable_function(
                contract_id=contract_id,
                function_name="depositRent",
                amount_hbar=amount,
                params=params
            )
            
        except Exception as e:
            print(f"❌ Rent deposit failed: {e}")
            return False
    
    def check_escrow_balance(self, tenant_id: str) -> Optional[float]:
        """Check escrowed rent amount for tenant"""
        if not self.is_available:
            return None
        
        try:
            contract_id = os.getenv('HEDERA_RENTESCROW_CONTRACT_ID')
            if not contract_id:
                return None
            
            params = ContractFunctionParameters()
            params.add_string(tenant_id)
            
            result = self.executor.call_contract_function(
                contract_id=contract_id,
                function_name="getEscrowedAmount",
                params=params
            )
            
            # Convert from contract units to HBAR
            if result:
                return float(result) / 10**8
            
            return None
            
        except Exception as e:
            print(f"❌ Failed to check escrow: {e}")
            return None
    
    # ========== PROPERTY NFT OPERATIONS ==========
    
    def create_property_nft(self, property_id: str, metadata_uri: str) -> Optional[str]:
        """
        Mint NFT for a property listing
        
        Args:
            property_id: Property identifier
            metadata_uri: IPFS or HTTP URI to property metadata
            
        Returns:
            NFT token ID if successful, None otherwise
        """
        if not self.is_available:
            return None
        
        try:
            contract_id = os.getenv('HEDERA_PROPERTYNFT_CONTRACT_ID')
            if not contract_id:
                print("❌ PropertyNFT contract not configured")
                return None
            
            params = ContractFunctionParameters()
            params.add_string(property_id)
            params.add_string(metadata_uri)
            
            result = self.executor.execute_payable_function(
                contract_id=contract_id,
                function_name="mint",
                amount_hbar=0.01,
                params=params
            )
            
            return str(result) if result else None
            
        except Exception as e:
            print(f"❌ NFT creation failed: {e}")
            return None
    
    # ========== LEASE AGREEMENT OPERATIONS ==========
    
    def create_lease_agreement(self, property_id: str, tenant_id: str,
                             monthly_rent: float, duration_months: int) -> bool:
        """
        Create a lease agreement on-chain
        
        Args:
            property_id: Property NFT ID
            tenant_id: Tenant account
            monthly_rent: Monthly rent in HBAR
            duration_months: Lease duration in months
            
        Returns:
            True if successful
        """
        if not self.is_available:
            return False
        
        try:
            contract_id = os.getenv('HEDERA_LEASEAGREEMENT_CONTRACT_ID')
            if not contract_id:
                print("❌ LeaseAgreement contract not configured")
                return False
            
            params = ContractFunctionParameters()
            params.add_uint256(int(property_id))
            params.add_address(tenant_id)
            params.add_uint256(int(monthly_rent * 10**8))
            params.add_uint256(duration_months)
            
            return self.executor.execute_payable_function(
                contract_id=contract_id,
                function_name="createLease",
                amount_hbar=0.01,
                params=params
            )
            
        except Exception as e:
            print(f"❌ Lease creation failed: {e}")
            return False
    
    # ========== REPUTATION SYSTEM ==========
    
    def update_reputation(self, user_id: str, reputation_score: int) -> bool:
        """Update user reputation on-chain.

        This method exists for backward compatibility and updates an overall
        reputation value if the contract supports it.
        """
        if not self.is_available:
            return False

        try:
            contract_id = os.getenv('HEDERA_REPUTATION_CONTRACT_ID')
            if not contract_id:
                print("❌ Reputation contract not configured")
                return False

            params = ContractFunctionParameters()
            params.add_address(user_id)
            params.add_uint256(reputation_score)

            return self.executor.execute_payable_function(
                contract_id=contract_id,
                function_name="updateReputation",
                amount_hbar=0.001,
                params=params
            )

        except Exception as e:
            print(f"❌ Reputation update failed: {e}")
            return False

    def update_reputation_components(
        self,
        user_id: str,
        payment_consistency: int,
        lease_completion_rate: int,
        reviews_score: int,
    ) -> bool:
        """Update detailed reputation components on-chain."""
        if not self.is_available:
            return False

        try:
            contract_id = os.getenv('HEDERA_REPUTATION_CONTRACT_ID')
            if not contract_id:
                print("❌ Reputation contract not configured")
                return False

            # Update each component (assuming the contract supports each call)
            for fn, value in [
                ("updatePaymentConsistency", payment_consistency),
                ("updateLeaseCompletionRate", lease_completion_rate),
                ("updateReviewsScore", reviews_score),
            ]:
                params = ContractFunctionParameters()
                params.add_address(user_id)
                params.add_uint256(int(value))
                self.executor.execute_payable_function(
                    contract_id=contract_id,
                    function_name=fn,
                    amount_hbar=0.0005,
                    params=params,
                )

            return True

        except Exception as e:
            print(f"❌ Reputation component update failed: {e}")
            return False
    
    def get_reputation(self, user_id: str) -> Optional[int]:
        """Get user reputation from contract"""
        if not self.is_available:
            return None
        
        try:
            contract_id = os.getenv('HEDERA_REPUTATION_CONTRACT_ID')
            if not contract_id:
                return None
            
            params = ContractFunctionParameters()
            params.add_address(user_id)
            
            result = self.executor.call_contract_function(
                contract_id=contract_id,
                function_name="getReputation",
                params=params
            )
            
            return int(result) if result else None
            
        except Exception as e:
            print(f"❌ Failed to get reputation: {e}")
            return None
    
    # ========== SAVINGS VAULT OPERATIONS ==========
    
    def deposit_to_savings(self, user_id: str, amount: float) -> bool:
        """Deposit to user's savings vault"""
        if not self.is_available:
            return False
        
        try:
            contract_id = os.getenv('HEDERA_SAVINGSVAULT_CONTRACT_ID')
            if not contract_id:
                return False
            
            params = ContractFunctionParameters()
            params.add_address(user_id)
            params.add_uint256(int(amount * 10**8))
            
            return self.executor.execute_payable_function(
                contract_id=contract_id,
                function_name="deposit",
                amount_hbar=amount,
                params=params
            )
            
        except Exception as e:
            print(f"❌ Savings deposit failed: {e}")
            return False
    
    def get_savings_balance(self, user_id: str) -> Optional[float]:
        """Get user's savings balance"""
        if not self.is_available:
            return None
        
        try:
            contract_id = os.getenv('HEDERA_SAVINGSVAULT_CONTRACT_ID')
            if not contract_id:
                return None
            
            params = ContractFunctionParameters()
            params.add_address(user_id)
            
            result = self.executor.call_contract_function(
                contract_id=contract_id,
                function_name="getBalance",
                params=params
            )
            
            if result:
                return float(result) / 10**8
            
            return None
            
        except Exception as e:
            print(f"❌ Failed to get savings: {e}")
            return None
    
    # ========== P2P COMMUNITY ==========
    
    def register_community_member(self, user_id: str, user_type: str) -> bool:
        """Register user in P2P community"""
        if not self.is_available:
            return False
        
        try:
            contract_id = os.getenv('HEDERA_P2PCOMMUNITY_CONTRACT_ID')
            if not contract_id:
                return False
            
            params = ContractFunctionParameters()
            params.add_address(user_id)
            params.add_string(user_type)  # "LANDLORD", "TENANT", "INVESTOR"
            
            return self.executor.execute_payable_function(
                contract_id=contract_id,
                function_name="registerUser",
                amount_hbar=0.001,
                params=params
            )
            
        except Exception as e:
            print(f"❌ Community registration failed: {e}")
            return False
    
    # ========== UTILITY METHODS ==========
    
    def is_blockchain_ready(self) -> bool:
        """Check if blockchain is properly configured and ready"""
        return self.is_available
    
    def get_contract_status(self) -> Dict[str, bool]:
        """Get status of all contracts"""
        status = {}
        contracts = [
            'FIND_TOKEN',
            'PROPERTYNFT',
            'LEASEAGREEMENT',
            'RENTESCROW',
            'SAVINGSVAULT',
            'REPUTATION',
            'P2PCOMMUNITY',
        ]
        
        for contract in contracts:
            contract_id = os.getenv(f'HEDERA_{contract}_CONTRACT_ID')
            status[contract] = bool(contract_id)
        
        return status
    
    def close(self):
        """Close executor connection"""
        if self.executor:
            self.executor.close()


# Global blockchain service instance
_blockchain_service: Optional[BlockchainService] = None


def get_blockchain_service() -> BlockchainService:
    """Get or create global blockchain service instance"""
    global _blockchain_service
    
    if _blockchain_service is None:
        _blockchain_service = BlockchainService()
    
    return _blockchain_service


# Example usage in AI agents:
#
# from backend.blockchain_service import get_blockchain_service
#
# class TenantAIAgent:
#     def __init__(self, user_id):
#         self.user_id = user_id
#         self.blockchain = get_blockchain_service()
#     
#     def pay_rent(self, amount: float) -> bool:
#         return self.blockchain.deposit_rent_payment(self.user_id, amount)
#     
#     def check_payment_status(self) -> Optional[float]:
#         return self.blockchain.check_escrow_balance(self.user_id)
