"""
Contract Deployment Module for Hedera
Handles deployment of smart contracts to Hedera testnet/mainnet
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

try:
    from hedera import (
        Client, AccountId, PrivateKey,
        ContractCreateFlow, Hbar, HbarUnit,
        FileCreateTransaction, ContractFunctionParameters,
    )
    HEDERA_AVAILABLE = True
except ImportError:
    HEDERA_AVAILABLE = False

load_dotenv()


class ContractDeployer:
    """Deploy smart contracts to Hedera network"""
    
    def __init__(self, account_id: str = None, private_key: str = None, network: str = "testnet"):
        """
        Initialize the contract deployer
        
        Args:
            account_id: Hedera account ID (format: 0.0.xxxxx)
            private_key: Account private key
            network: 'testnet' or 'mainnet'
        """
        self.account_id = account_id or os.getenv('HEDERA_ACCOUNT_ID', '0.0.0')
        self.private_key_str = private_key or os.getenv('HEDERA_PRIVATE_KEY', '')
        self.network = network
        self.client = None
        self.deployed_contracts: Dict[str, Dict] = {}
        
        if HEDERA_AVAILABLE:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Hedera client"""
        try:
            if self.network == "testnet":
                self.client = Client.for_testnet()
            else:
                self.client = Client.for_mainnet()
            
            if self.account_id and self.private_key_str:
                operator_id = AccountId.from_string(self.account_id)
                operator_key = PrivateKey.from_string(self.private_key_str)
                self.client.set_operator(operator_id, operator_key)
                print(f"✅ Hedera client initialized for {self.account_id}")
        except Exception as e:
            print(f"❌ Failed to initialize Hedera client: {e}")
            self.client = None
    
    def deploy_contract_from_bytecode(
        self,
        contract_name: str,
        bytecode: str,
        constructor_params: Optional[ContractFunctionParameters] = None,
        gas_limit: int = 2_000_000
    ) -> Optional[Tuple[str, str]]:
        """
        Deploy a smart contract from bytecode
        
        Args:
            contract_name: Name of the contract
            bytecode: Compiled contract bytecode
            constructor_params: Constructor parameters
            gas_limit: Gas limit for deployment
            
        Returns:
            Tuple of (contract_id, file_id) or None if deployment fails
        """
        if not self.client:
            print("❌ Hedera client not initialized")
            return None
        
        try:
            print(f"📦 Deploying contract: {contract_name}")
            
            # Create contract flow
            contract_tx = ContractCreateFlow()
            contract_tx.set_gas(gas_limit)
            contract_tx.set_bytecode(bytes.fromhex(bytecode.replace('0x', '')))
            
            if constructor_params:
                contract_tx.set_constructor_parameters(constructor_params)
            
            # Execute deployment transaction
            contract_rx = contract_tx.execute(self.client)
            contract_receipt = contract_rx.get_receipt(self.client)
            
            contract_id = str(contract_receipt.contract_id)
            file_id = str(contract_receipt.file_id) if hasattr(contract_receipt, 'file_id') else None
            
            # Store deployment info
            self.deployed_contracts[contract_name] = {
                'contract_id': contract_id,
                'file_id': file_id,
                'bytecode_hash': hash(bytecode),
                'network': self.network,
                'transaction_id': str(contract_rx.transaction_id)
            }
            
            print(f"✅ Contract deployed successfully: {contract_id}")
            return contract_id, file_id
            
        except Exception as e:
            print(f"❌ Contract deployment failed: {e}")
            return None
    
    def deploy_from_solidity_file(
        self,
        sol_file_path: str,
        contract_name: str,
        bytecode_hex: str,
        constructor_params: Optional[ContractFunctionParameters] = None,
        gas_limit: int = 2_000_000
    ) -> Optional[Tuple[str, str]]:
        """
        Deploy a contract from a Solidity file using precompiled bytecode
        
        Args:
            sol_file_path: Path to the Solidity source file
            contract_name: Name of the contract
            bytecode_hex: Hex-encoded bytecode from compiler
            constructor_params: Constructor parameters
            gas_limit: Gas limit for deployment
            
        Returns:
            Tuple of (contract_id, file_id) or None
        """
        if not Path(sol_file_path).exists():
            print(f"❌ Solidity file not found: {sol_file_path}")
            return None
        
        return self.deploy_contract_from_bytecode(
            contract_name=contract_name,
            bytecode=bytecode_hex,
            constructor_params=constructor_params,
            gas_limit=gas_limit
        )
    
    def get_deployment_info(self, contract_name: str) -> Optional[Dict]:
        """Get information about a deployed contract"""
        return self.deployed_contracts.get(contract_name)
    
    def save_deployments(self, output_file: str = "deployments.json"):
        """Save deployment information to a JSON file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.deployed_contracts, f, indent=2)
            print(f"✅ Deployments saved to {output_file}")
        except Exception as e:
            print(f"❌ Failed to save deployments: {e}")
    
    def load_deployments(self, input_file: str = "deployments.json"):
        """Load deployment information from a JSON file"""
        try:
            with open(input_file, 'r') as f:
                self.deployed_contracts = json.load(f)
            print(f"✅ Deployments loaded from {input_file}")
        except Exception as e:
            print(f"❌ Failed to load deployments: {e}")


def deploy_find_token(
    ecosystem_addr: str,
    staking_addr: str,
    team_addr: str,
    treasury_addr: str,
    partners_addr: str,
    liquidity_addr: str,
    public_sale_addr: str,
    bytecode_hex: str,
    network: str = "testnet"
) -> Optional[str]:
    """
    Deploy the FIND token contract with allocation addresses
    
    Args:
        ecosystem_addr: Ecosystem fund address
        staking_addr: Staking fund address
        team_addr: Team fund address
        treasury_addr: Treasury address
        partners_addr: Partners address
        liquidity_addr: Liquidity address
        public_sale_addr: Public sale address
        bytecode_hex: Compiled bytecode
        network: Network to deploy to
        
    Returns:
        Contract ID if successful, None otherwise
    """
    deployer = ContractDeployer(network=network)
    
    if not deployer.client:
        print("❌ Cannot deploy: Hedera client not available")
        return None
    
    try:
        # Create constructor parameters
        params = ContractFunctionParameters()
        params.add_address(ecosystem_addr)
        params.add_address(staking_addr)
        params.add_address(team_addr)
        params.add_address(treasury_addr)
        params.add_address(partners_addr)
        params.add_address(liquidity_addr)
        params.add_address(public_sale_addr)
        
        # Deploy contract
        result = deployer.deploy_contract_from_bytecode(
            contract_name="FindToken",
            bytecode=bytecode_hex,
            constructor_params=params,
            gas_limit=5_000_000  # Higher gas for complex token initialization
        )
        
        if result:
            contract_id, file_id = result
            deployer.save_deployments()
            return contract_id
        
    except Exception as e:
        print(f"❌ FIND token deployment failed: {e}")
    
    return None


if __name__ == "__main__":
    # Example usage
    deployer = ContractDeployer(network="testnet")
    
    # Check if deployment is possible
    if deployer.client:
        print("✅ Contract deployer ready for operations")
    else:
        print("⚠️  Hedera SDK not available - deployment would use mock mode")
