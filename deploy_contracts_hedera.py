#!/usr/bin/env python
"""
Deploy FIND-RLB Contracts to Hedera Testnet
Practical deployment script with error handling and reporting
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.hedera_contract_deployment import (
    HederaContractDeployer,
    deploy_all_contracts,
    _load_contract_bytecode
)


def save_deployment_results(results: dict, filename: str = "deployment_results.json"):
    """Save deployment results to JSON file"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "network": "testnet",
        "contracts": results,
        "env_updates": {
            f"HEDERA_{name.upper()}_CONTRACT_ID": contract_id
            for name, contract_id in results.items()
            if contract_id
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Results saved to {filename}")
    return output


def print_deployment_report(results: dict):
    """Print deployment report"""
    print("\n" + "="*70)
    print("FIND-RLB SMART CONTRACT DEPLOYMENT REPORT")
    print("="*70)
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nTotal Contracts: {total}")
    print(f"Successfully Deployed: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {(successful/total*100):.1f}%\n")
    
    print("CONTRACT DETAILS:")
    print("-" * 70)
    
    for contract_name, contract_id in results.items():
        status = "✅" if contract_id else "❌"
        print(f"{status} {contract_name:25} {contract_id or 'Failed'}")
    
    print("="*70)
    
    if successful == total:
        print("\n🎉 ALL CONTRACTS DEPLOYED SUCCESSFULLY!\n")
    else:
        print(f"\n⚠️  {total - successful} contract(s) failed deployment\n")


def update_env_file(results: dict):
    """Update .env file with deployed contract IDs"""
    env_file = Path(__file__).parent.parent / ".env"
    
    if not env_file.exists():
        print(f"⚠️  .env file not found at {env_file}")
        return
    
    try:
        # Read current .env
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Create set of contract env vars to update
        contract_env_keys = {f"HEDERA_{name.upper()}_CONTRACT_ID" for name in results.keys()}
        
        # Remove existing contract ID lines
        new_lines = [line for line in lines if not any(
            line.startswith(f"{key}=") for key in contract_env_keys
        )]
        
        # Add new contract IDs
        new_lines.append("\n# Smart Contract Deployments (Auto-updated)\n")
        for contract_name, contract_id in results.items():
            if contract_id:
                key = f"HEDERA_{contract_name.upper()}_CONTRACT_ID"
                new_lines.append(f"{key}={contract_id}\n")
        
        # Write back
        with open(env_file, 'w') as f:
            f.writelines(new_lines)
        
        print(f"✅ Updated .env file with contract IDs")
        
    except Exception as e:
        print(f"❌ Failed to update .env: {e}")


def verify_deployment(deployer: HederaContractDeployer, contract_id: str,
                     contract_name: str) -> bool:
    """Verify a deployed contract is accessible"""
    try:
        # Try to read contract info
        from hedera import ContractInfoQuery, ContractId
        query = ContractInfoQuery()
        query.set_contract_id(ContractId.from_string(contract_id))
        info = query.execute(deployer.client)
        print(f"  ✓ Contract verified and accessible")
        return True
    except Exception as e:
        print(f"  ✗ Verification failed: {str(e)[:50]}")
        return False


def main():
    """Main deployment function"""
    print("\n" + "="*70)
    print("FIND-RLB SMART CONTRACT DEPLOYMENT TOOL")
    print("="*70)
    
    # Check prerequisites
    print("\nChecking prerequisites...")
    
    account_id = os.getenv('HEDERA_ACCOUNT_ID')
    private_key = os.getenv('HEDERA_PRIVATE_KEY')
    
    if not account_id or not private_key:
        print("❌ Missing Hedera credentials in .env")
        print("   Required: HEDERA_ACCOUNT_ID, HEDERA_PRIVATE_KEY")
        return 1
    
    print(f"✅ Account ID: {account_id}")
    print(f"✅ Private Key: {'*' * 20}...")
    print(f"✅ Network: testnet")
    
    # Check if bytecode is available
    print("\nChecking contract bytecode...")
    contracts_to_deploy = [
        'FindToken', 'PropertyNFT', 'LeaseAgreement',
        'RentEscrow', 'SavingsVault', 'Reputation', 'P2PCommunity'
    ]
    
    missing_bytecode = []
    for contract in contracts_to_deploy:
        bytecode = _load_contract_bytecode(contract)
        if not bytecode:
            missing_bytecode.append(contract)
        else:
            print(f"✅ {contract}")
    
    if missing_bytecode:
        print(f"\n⚠️  Missing bytecode for: {', '.join(missing_bytecode)}")
        print("   Compile with: cd contracts && npx hardhat compile")
    
    # Confirm deployment
    print("\n" + "-"*70)
    response = input("Ready to deploy contracts to Hedera testnet? (y/N): ").strip().lower()
    
    if response != 'y':
        print("Deployment cancelled.")
        return 0
    
    print("\n" + "="*70)
    print("DEPLOYING CONTRACTS...")
    print("="*70 + "\n")
    
    # Deploy contracts
    results = deploy_all_contracts()
    
    # Generate reports
    print_deployment_report(results)
    
    # Save results
    deployment_info = save_deployment_results(results)
    
    # Update .env file
    update_env_file(results)
    
    # Show next steps
    print("\n📋 NEXT STEPS:")
    print("-" * 70)
    print("1. Verify deployment results in deployment_results.json")
    print("2. Update contract addresses in frontend configuration")
    print("3. Test contract interactions with example scripts")
    print("4. Configure AI agents with contract addresses")
    print("5. Deploy to production when ready")
    print("-" * 70 + "\n")
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
