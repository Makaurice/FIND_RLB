"""
Hedera Smart Contract Deployment Module
Deploys and interacts with Solidity contracts on Hedera testnet/mainnet
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

try:
    from hedera import (
        Client, AccountId, PrivateKey,
        ContractCreateFlow, ContractExecuteTransaction,
        ContractCallQuery, ContractId,
        Hbar, HbarUnit, TransactionId,
        ContractFunctionParameters,
    )
    HEDERA_AVAILABLE = True
except ImportError:
    HEDERA_AVAILABLE = False
    print("⚠️ Hedera SDK not available")


class HederaContractDeployer:
    """Deploy and interact with smart contracts on Hedera"""
    
    def __init__(self, operator_id: str = None, operator_key: str = None, network: str = "testnet"):
        """
        Initialize contract deployer
        
        Args:
            operator_id: Operator account ID (0.0.xxxxx)
            operator_key: Operator private key
            network: 'testnet' or 'mainnet'
        """
        load_dotenv()
        
        self.operator_id = operator_id or os.getenv('HEDERA_ACCOUNT_ID')
        self.operator_key = operator_key or os.getenv('HEDERA_PRIVATE_KEY')
        self.network = network
        self.client = None
        self.deployed_contracts: Dict[str, Dict[str, Any]] = {}
        
        if HEDERA_AVAILABLE and self.operator_id and self.operator_key:
            self._init_client()
        
    def _init_client(self):
        """Initialize Hedera client"""
        try:
            if self.network == "testnet":
                self.client = Client.for_testnet()
            elif self.network == "mainnet":
                self.client = Client.for_mainnet()
            else:
                self.client = Client.for_testnet()
            
            # Set operator
            account_id = AccountId.from_string(self.operator_id)
            private_key = PrivateKey.from_string(self.operator_key)
            self.client.set_operator(account_id, private_key)
            
            print(f"✅ Hedera client initialized for account {self.operator_id} on {self.network}")
        except Exception as e:
            print(f"❌ Failed to initialize Hedera client: {e}")
            self.client = None
    
    def deploy_contract(self, name: str, bytecode: str, gas: int = 2_000_000,
                       constructor_params: Optional[ContractFunctionParameters] = None) -> Optional[ContractId]:
        """
        Deploy a smart contract to Hedera
        
        Args:
            name: Contract name for tracking
            bytecode: Compiled contract bytecode (hex string)
            gas: Gas limit for deployment
            constructor_params: Optional constructor parameters
            
        Returns:
            ContractId if successful, None otherwise
        """
        if not self.client:
            print("❌ Hedera client not initialized")
            return None
        
        try:
            # Convert bytecode hex string to bytes if needed
            if isinstance(bytecode, str):
                bytecode = bytes.fromhex(bytecode.replace('0x', ''))
            
            # Create contract deployment flow
            deploy_flow = ContractCreateFlow()
            deploy_flow.set_gas(gas)
            deploy_flow.set_bytecode(bytecode)
            
            if constructor_params:
                deploy_flow.set_constructor_parameters(constructor_params)
            
            # Execute deployment
            tx_response = deploy_flow.execute(self.client)
            
            # Get receipt
            receipt = tx_response.get_receipt(self.client)
            contract_id = receipt.contract_id
            
            # Store deployment info
            self.deployed_contracts[name] = {
                'contract_id': str(contract_id),
                'transaction_id': str(receipt.transaction_id),
                'gas_used': receipt.gas_used if hasattr(receipt, 'gas_used') else None,
            }
            
            print(f"✅ Contract {name} deployed: {contract_id}")
            return contract_id
            
        except Exception as e:
            print(f"❌ Failed to deploy contract {name}: {e}")
            return None
    
    def execute_contract_function(self, contract_id: str, function_name: str,
                                 gas: int = 500_000, amount: float = 0.0,
                                 params: Optional[ContractFunctionParameters] = None) -> Optional[Any]:
        """
        Execute a function in a deployed smart contract
        
        Args:
            contract_id: Target contract ID
            function_name: Function name to call
            gas: Gas limit for execution
            amount: HBAR amount to send (payable functions)
            params: Function parameters
            
        Returns:
            Function result if successful, None otherwise
        """
        if not self.client:
            print("❌ Hedera client not initialized")
            return None
        
        try:
            contract_id_obj = ContractId.from_string(contract_id)
            
            # Create execute transaction
            execute_tx = ContractExecuteTransaction()
            execute_tx.set_contract_id(contract_id_obj)
            execute_tx.set_function_name(function_name)
            execute_tx.set_gas(gas)
            
            if amount > 0:
                execute_tx.set_payable_amount(Hbar(amount, HbarUnit.HBAR))
            
            if params:
                execute_tx.set_function_parameters(params)
            
            # Execute
            tx_response = execute_tx.execute(self.client)
            receipt = tx_response.get_receipt(self.client)
            
            print(f"✅ Function {function_name} executed successfully")
            return receipt
            
        except Exception as e:
            print(f"❌ Failed to execute function {function_name}: {e}")
            return None
    
    def read_contract_state(self, contract_id: str, function_name: str,
                           params: Optional[ContractFunctionParameters] = None) -> Optional[Any]:
        """
        Read contract state (view/pure function)
        
        Args:
            contract_id: Target contract ID
            function_name: Function name to call
            params: Function parameters
            
        Returns:
            Query result if successful, None otherwise
        """
        if not self.client:
            print("❌ Hedera client not initialized")
            return None
        
        try:
            contract_id_obj = ContractId.from_string(contract_id)
            
            # Create query
            query = ContractCallQuery()
            query.set_contract_id(contract_id_obj)
            query.set_gas(100_000)
            query.set_function_name(function_name)
            
            if params:
                query.set_function_parameters(params)
            
            # Execute query
            result = query.execute(self.client)
            
            print(f"✅ Function {function_name} read successfully")
            return result
            
        except Exception as e:
            print(f"❌ Failed to read function {function_name}: {e}")
            return None
    
    def get_deployed_contracts(self) -> Dict[str, Dict[str, Any]]:
        """Get all deployed contracts info"""
        return self.deployed_contracts
    
    def close(self):
        """Close the Hedera client connection"""
        if self.client:
            self.client.close()


class FindTokenDeployer(HederaContractDeployer):
    """Specialized deployer for FIND token contract"""
    
    def deploy_find_token(self, initial_supply: int = 1_000_000_000,
                         decimals: int = 8) -> Optional[ContractId]:
        """
        Deploy the FIND token contract
        
        Args:
            initial_supply: Initial token supply
            decimals: Token decimals
            
        Returns:
            ContractId if successful, None otherwise
        """
        bytecode = self._get_find_token_bytecode()
        
        if not bytecode:
            print("❌ Failed to get FIND token bytecode")
            return None
        
        # Constructor params for token initialization
        params = ContractFunctionParameters()
        params.add_uint256(initial_supply)
        params.add_uint8(decimals)
        
        return self.deploy_contract(
            "FIND_Token",
            bytecode,
            gas=3_000_000,
            constructor_params=params
        )
    
    def _get_find_token_bytecode(self) -> Optional[str]:
        """Load FIND token bytecode from compiled artifacts"""
        try:
            # Try to load from hardhat artifacts
            import json
            artifact_path = "contracts/artifacts/FindToken.json"
            if os.path.exists(artifact_path):
                with open(artifact_path, 'r') as f:
                    artifact = json.load(f)
                    return artifact.get('bytecode', artifact.get('deployedBytecode'))
            
            print(f"⚠️ Artifact not found at {artifact_path}")
            return None
            
        except Exception as e:
            print(f"❌ Failed to load bytecode: {e}")
            return None


def deploy_all_contracts() -> Dict[str, Optional[str]]:
    """
    Deploy all FIND-RLB contracts to Hedera testnet
    
    Returns:
        Dictionary mapping contract names to their deployed contract IDs
    """
    deployer = HederaContractDeployer()
    
    if not deployer.client:
        print("❌ Cannot deploy: Hedera client not initialized")
        return {}
    
    results = {}
    
    # Contract names and their configurations
    contracts = [
        ('PropertyNFT', 2_000_000),
        ('LeaseAgreement', 2_000_000),
        ('RentEscrow', 1_500_000),
        ('SavingsVault', 1_500_000),
        ('Reputation', 1_000_000),
        ('P2PCommunity', 1_200_000),
    ]
    
    print("\n" + "="*60)
    print("DEPLOYING FIND-RLB SMART CONTRACTS")
    print("="*60 + "\n")
    
    for contract_name, gas_limit in contracts:
        print(f"Deploying {contract_name}...")
        bytecode = _load_contract_bytecode(contract_name)
        
        if bytecode:
            contract_id = deployer.deploy_contract(contract_name, bytecode, gas=gas_limit)
            if contract_id:
                results[contract_name] = str(contract_id)
                print(f"  ✅ Deployed: {contract_id}\n")
            else:
                results[contract_name] = None
                print(f"  ❌ Deployment failed\n")
        else:
            results[contract_name] = None
            print(f"  ❌ Bytecode not available\n")
    
    deployer.close()
    
    return results


def _load_contract_bytecode(contract_name: str) -> Optional[str]:
    """Load contract bytecode from artifacts or return mock"""
    try:
        import json
        artifact_path = f"contracts/artifacts/{contract_name}.json"
        if os.path.exists(artifact_path):
            with open(artifact_path, 'r') as f:
                artifact = json.load(f)
                return artifact.get('bytecode', artifact.get('deployedBytecode'))
    except Exception as e:
        print(f"  ⚠️ Could not load bytecode for {contract_name}: {e}")
    
    return None


if __name__ == "__main__":
    # Deploy all contracts
    results = deploy_all_contracts()
    
    print("\n" + "="*60)
    print("DEPLOYMENT SUMMARY")
    print("="*60)
    
    for contract_name, contract_id in results.items():
        status = "✅" if contract_id else "❌"
        print(f"{status} {contract_name}: {contract_id or 'Failed'}")
    
    print("="*60)
