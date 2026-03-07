"""
Hedera Smart Contract Execution Examples
Demonstrates calling contracts with HBAR and HTS token interactions
"""

import os
from typing import Optional
from dotenv import load_dotenv

try:
    from hedera import (
        Client, AccountId, PrivateKey,
        ContractExecuteTransaction, ContractCallQuery,
        ContractId, ContractFunctionParameters,
        Hbar, HbarUnit,
        TokenCreateTransaction, TokenAssociateTransaction,
        TokenId, TokenType, TokenSupplyType,
        TransferTransaction, Transfer,
    )
    HEDERA_AVAILABLE = True
except ImportError:
    HEDERA_AVAILABLE = False


class HederaContractExecutor:
    """Execute functions in deployed Hedera smart contracts"""
    
    def __init__(self, operator_id: str = None, operator_key: str = None):
        """Initialize contract executor"""
        load_dotenv()
        
        self.operator_id = operator_id or os.getenv('HEDERA_ACCOUNT_ID')
        self.operator_key = operator_key or os.getenv('HEDERA_PRIVATE_KEY')
        self.client = None
        
        if HEDERA_AVAILABLE and self.operator_id and self.operator_key:
            self._init_client()
    
    def _init_client(self):
        """Initialize Hedera client"""
        try:
            self.client = Client.for_testnet()
            account_id = AccountId.from_string(self.operator_id)
            private_key = PrivateKey.from_string(self.operator_key)
            self.client.set_operator(account_id, private_key)
            print(f"✅ Executor initialized for {self.operator_id}")
        except Exception as e:
            print(f"❌ Failed to initialize executor: {e}")
            self.client = None
    
    def execute_payable_function(self, contract_id: str, function_name: str,
                                amount_hbar: float,
                                params: Optional[ContractFunctionParameters] = None) -> bool:
        """
        Execute payable contract function with HBAR
        
        Example: Deposit rent payment into escrow
        """
        if not self.client:
            print("❌ Client not initialized")
            return False
        
        try:
            contract_id_obj = ContractId.from_string(contract_id)
            
            tx = ContractExecuteTransaction()
            tx.set_contract_id(contract_id_obj)
            tx.set_gas(500_000)
            tx.set_payable_amount(Hbar(amount_hbar, HbarUnit.HBAR))
            tx.set_function_name(function_name)
            
            if params:
                tx.set_function_parameters(params)
            
            response = tx.execute(self.client)
            receipt = response.get_receipt(self.client)
            
            print(f"✅ Payable function {function_name} executed")
            print(f"   Amount: {amount_hbar} HBAR")
            print(f"   Receipt: {receipt.transaction_id}")
            return True
            
        except Exception as e:
            print(f"❌ Execution failed: {e}")
            return False
    
    def create_hts_token(self, token_name: str, token_symbol: str,
                        initial_supply: int,
                        decimals: int = 8) -> Optional[TokenId]:
        """
        Create an HTS token on Hedera
        
        Example: Create rental payment token
        """
        if not self.client:
            print("❌ Client not initialized")
            return None
        
        try:
            tx = TokenCreateTransaction()
            tx.set_name(token_name)
            tx.set_symbol(token_symbol)
            tx.set_treasury_account_id(AccountId.from_string(self.operator_id))
            tx.set_token_type(TokenType.FUNGIBLE_COMMON)
            tx.set_decimals(decimals)
            tx.set_initial_supply(initial_supply)
            tx.set_supply_type(TokenSupplyType.INFINITE)
            
            response = tx.execute(self.client)
            receipt = response.get_receipt(self.client)
            token_id = receipt.token_id
            
            print(f"✅ HTS Token created: {token_id}")
            print(f"   Name: {token_name}")
            print(f"   Symbol: {token_symbol}")
            print(f"   Supply: {initial_supply} (decimals: {decimals})")
            return token_id
            
        except Exception as e:
            print(f"❌ Token creation failed: {e}")
            return None
    
    def associate_token(self, account_id: str, token_id: str) -> bool:
        """
        Associate account with HTS token
        
        Required before transferring tokens to account
        """
        if not self.client:
            print("❌ Client not initialized")
            return False
        
        try:
            tx = TokenAssociateTransaction()
            tx.set_account_id(AccountId.from_string(account_id))
            tx.add_token_id(TokenId.from_string(token_id))
            
            response = tx.execute(self.client)
            receipt = response.get_receipt(self.client)
            
            print(f"✅ Token associated")
            print(f"   Account: {account_id}")
            print(f"   Token: {token_id}")
            return True
            
        except Exception as e:
            print(f"❌ Association failed: {e}")
            return False
    
    def transfer_token(self, token_id: str, from_account: str,
                      to_account: str, amount: int) -> bool:
        """
        Transfer HTS tokens between accounts
        """
        if not self.client:
            print("❌ Client not initialized")
            return False
        
        try:
            tx = TransferTransaction()
            tx.add_token_transfer(
                TokenId.from_string(token_id),
                AccountId.from_string(from_account),
                -amount
            )
            tx.add_token_transfer(
                TokenId.from_string(token_id),
                AccountId.from_string(to_account),
                amount
            )
            
            response = tx.execute(self.client)
            receipt = response.get_receipt(self.client)
            
            print(f"✅ Token transfer successful")
            print(f"   Token: {token_id}")
            print(f"   From: {from_account}")
            print(f"   To: {to_account}")
            print(f"   Amount: {amount}")
            return True
            
        except Exception as e:
            print(f"❌ Transfer failed: {e}")
            return False
    
    def call_contract_function(self, contract_id: str, function_name: str,
                              gas: int = 100_000,
                              params: Optional[ContractFunctionParameters] = None) -> Optional[Any]:
        """
        Call a view/pure function to read contract state
        """
        if not self.client:
            print("❌ Client not initialized")
            return None
        
        try:
            query = ContractCallQuery()
            query.set_contract_id(ContractId.from_string(contract_id))
            query.set_gas(gas)
            query.set_function_name(function_name)
            
            if params:
                query.set_function_parameters(params)
            
            result = query.execute(self.client)
            
            print(f"✅ Function {function_name} called successfully")
            return result
            
        except Exception as e:
            print(f"❌ Function call failed: {e}")
            return None
    
    def close(self):
        """Close client connection"""
        if self.client:
            self.client.close()


# Example workflows for FIND-RLB

def example_rent_escrow_workflow():
    """
    Example: Tenant deposits rent into escrow contract
    """
    print("\n" + "="*60)
    print("EXAMPLE: RENT ESCROW WORKFLOW")
    print("="*60 + "\n")
    
    executor = HederaContractExecutor()
    
    if not executor.client:
        print("Cannot run example without Hedera client")
        return
    
    # Assume we have a deployed RentEscrow contract
    escrow_contract_id = os.getenv('HEDERA_RENTESCROW_CONTRACT_ID')
    tenant_account = os.getenv('HEDERA_ACCOUNT_ID')
    monthly_rent_hbar = 10.0  # 10 HBAR per month
    
    if not escrow_contract_id:
        print("⚠️  RentEscrow contract ID not configured")
        executor.close()
        return
    
    print(f"Contract: {escrow_contract_id}")
    print(f"Tenant: {tenant_account}")
    print(f"Amount: {monthly_rent_hbar} HBAR\n")
    
    # Step 1: Deposit rent payment
    params = ContractFunctionParameters()
    params.add_string(tenant_account)  # target address
    params.add_uint256(int(monthly_rent_hbar * 1e8))  # amount in tinybars
    
    executor.execute_payable_function(
        escrow_contract_id,
        "depositRent",
        monthly_rent_hbar,
        params
    )
    
    executor.close()


def example_hts_token_workflow():
    """
    Example: Create and transfer HTS tokens for rewards
    """
    print("\n" + "="*60)
    print("EXAMPLE: HTS TOKEN WORKFLOW")
    print("="*60 + "\n")
    
    executor = HederaContractExecutor()
    
    if not executor.client:
        print("Cannot run example without Hedera client")
        return
    
    # Create FIND reward token
    token_id = executor.create_hts_token(
        "FIND Rewards",
        "FIND-R",
        1_000_000_000,  # 1 billion initial supply
        8
    )
    
    if not token_id:
        print("Failed to create token")
        executor.close()
        return
    
    print(f"\nToken ID: {token_id}")
    print(f"Stored for later use: HEDERA_FINDREWARDS_TOKEN_ID={token_id}")
    
    executor.close()


if __name__ == "__main__":
    print("\n🚀 HEDERA SMART CONTRACT EXECUTION EXAMPLES\n")
    
    # Run examples
    try:
        example_rent_escrow_workflow()
    except Exception as e:
        print(f"❌ Example failed: {e}")
    
    try:
        example_hts_token_workflow()
    except Exception as e:
        print(f"❌ Example failed: {e}")
    
    print("\n" + "="*60)
    print("Examples completed")
    print("="*60 + "\n")
