"""
Hedera Integration Guide for FIND-RLB
Complete implementation guide for smart contract deployment and execution
"""

# ============================================================================
# PART 1: SMART CONTRACT DEPLOYMENT
# ============================================================================

"""
Step 1: Compile Solidity Contracts

To compile your contracts, ensure Hardhat is configured:

$ cd contracts
$ npm install  # Already done
$ npx hardhat compile

This generates:
- artifacts/FindToken.json
- artifacts/PropertyNFT.json
- artifacts/LeaseAgreement.json
- artifacts/RentEscrow.json
- artifacts/SavingsVault.json
- artifacts/Reputation.json
- artifacts/P2PCommunity.json

Each artifact contains the "bytecode" field needed for deployment.
"""

# ============================================================================
# PART 2: ENVIRONMENT CONFIGURATION
# ============================================================================

"""
Ensure your .env file contains:

# Hedera Account
HEDERA_ACCOUNT_ID=0.0.7974203
HEDERA_PRIVATE_KEY=302e020100300506092a864886f70d0101050420...
HEDERA_NETWORK=testnet

# Deployed Contract Addresses (populated after deployment)
HEDERA_FIND_TOKEN_CONTRACT_ID=0.0.xxxxx
HEDERA_PROPERTYNFT_CONTRACT_ID=0.0.xxxxx
HEDERA_LEASEAGREEMENT_CONTRACT_ID=0.0.xxxxx
HEDERA_RENTESCROW_CONTRACT_ID=0.0.xxxxx
HEDERA_SAVINGSVAULT_CONTRACT_ID=0.0.xxxxx
HEDERA_REPUTATION_CONTRACT_ID=0.0.xxxxx
HEDERA_P2PCOMMUNITY_CONTRACT_ID=0.0.xxxxx

# HTS Token IDs (if using native Hedera tokens)
HEDERA_FINDREWARDS_TOKEN_ID=0.0.xxxxx
"""

# ============================================================================
# PART 3: DEPLOYMENT WORKFLOW
# ============================================================================

"""
Python Deployment Script:

from backend.hedera_contract_deployment import deploy_all_contracts

# Deploy all contracts to Hedera testnet
results = deploy_all_contracts()

for contract_name, contract_id in results.items():
    if contract_id:
        print(f"✅ {contract_name}: {contract_id}")
        # Save to .env:
        # HEDERA_[NAME]_CONTRACT_ID={contract_id}
    else:
        print(f"❌ {contract_name}: Failed to deploy")
"""

# ============================================================================
# PART 4: CONTRACT INTERACTION PATTERNS
# ============================================================================

"""
A. Tenant Deposits Rent (Payable Function)

from backend.hedera_contract_executor import HederaContractExecutor
from hedera import ContractFunctionParameters

executor = HederaContractExecutor()

# Parameters: tenant address, amount in tinybars
params = ContractFunctionParameters()
params.add_address(tenant_account.to_solidity_address())
params.add_int64(1000 * 10**8)  # 1000 tokens with 8 decimals

# Execute with HBAR payment (rent escrow fee)
executor.execute_payable_function(
    contract_id="0.0.12345",
    function_name="depositRent",
    amount_hbar=10.0,
    params=params
)

executor.close()
"""

# ============================================================================
# PART 5: HTS TOKEN INTEGRATION
# ============================================================================

"""
Create and Use Hedera Token Service (HTS) Tokens:

from backend.hedera_contract_executor import HederaContractExecutor

executor = HederaContractExecutor()

# Create a new HTS token for rent payments
token_id = executor.create_hts_token(
    token_name="Property Rent Token",
    token_symbol="PRENT",
    initial_supply=100_000_000,
    decimals=8
)

# Show token ID: 0.0.xxxxx

# Associate user account with token (required before transfers)
executor.associate_token(
    account_id="0.0.98765",
    token_id=str(token_id)
)

# Transfer tokens
executor.transfer_token(
    token_id=str(token_id),
    from_account="0.0.7974203",  # treasury
    to_account="0.0.98765",      # recipient
    amount=1000 * 10**8           # 1000 tokens
)

executor.close()
"""

# ============================================================================
# PART 6: AI AGENT INTEGRATION WITH BLOCKCHAIN
# ============================================================================

"""
In your AI agents (tenant_agent.py, landlord_agent.py, etc.):

from backend.hedera_contract_executor import HederaContractExecutor
from hedera import ContractFunctionParameters

class TenantAIAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.executor = HederaContractExecutor()
    
    def pay_rent(self, rent_amount: float, contract_id: str):
        '''Execute rent payment on blockchain'''
        params = ContractFunctionParameters()
        params.add_string(self.user_id)
        params.add_uint256(int(rent_amount * 10**8))
        
        return self.executor.execute_payable_function(
            contract_id=contract_id,
            function_name="depositRent",
            amount_hbar=rent_amount,
            params=params
        )
    
    def check_payment_status(self, contract_id: str):
        '''Read payment status from blockchain'''
        params = ContractFunctionParameters()
        params.add_string(self.user_id)
        
        return self.executor.call_contract_function(
            contract_id=contract_id,
            function_name="getPaymentStatus",
            params=params
        )
"""

# ============================================================================
# PART 7: API ENDPOINTS
# ============================================================================

"""
In backend/api_views.py:

from rest_framework.views import APIView
from backend.hedera_contract_executor import HederaContractExecutor
from hedera import ContractFunctionParameters

class RentPaymentView(APIView):
    def post(self, request):
        '''Process rent payment via blockchain'''
        tenant_id = request.data.get('tenant_id')
        amount = request.data.get('amount')
        contract_id = os.getenv('HEDERA_RENTESCROW_CONTRACT_ID')
        
        executor = HederaContractExecutor()
        
        params = ContractFunctionParameters()
        params.add_address(tenant_id)
        params.add_uint256(int(amount * 10**8))
        
        success = executor.execute_payable_function(
            contract_id=contract_id,
            function_name="depositRent",
            amount_hbar=amount,
            params=params
        )
        
        executor.close()
        
        return Response({
            'success': success,
            'message': 'Payment processed on Hedera blockchain'
        })

class PaymentStatusView(APIView):
    def get(self, request):
        '''Check payment status from blockchain'''
        tenant_id = request.query_params.get('tenant_id')
        contract_id = os.getenv('HEDERA_RENTESCROW_CONTRACT_ID')
        
        executor = HederaContractExecutor()
        
        params = ContractFunctionParameters()
        params.add_address(tenant_id)
        
        status = executor.call_contract_function(
            contract_id=contract_id,
            function_name="getEscrowedAmount",
            params=params
        )
        
        executor.close()
        
        return Response({
            'status': status,
            'contract': contract_id
        })
"""

# ============================================================================
# PART 8: FULL END-TO-END EXAMPLE
# ============================================================================

"""
Complete workflow for a rent payment:

1. User initiates rent payment via frontend
   POST /api/rent-payment/
   {
       "tenant_id": "0.0.98765",
       "amount": 10.0
   }

2. Backend API receives request:
   - Validates tenant account
   - Checks contract deployment
   - Calls HederaContractExecutor

3. Smart Contract Execution:
   - ContractExecuteTransaction created
   - gas: 500,000
   - payable_amount: 10 HBAR
   - function: depositRent(address, uint256)
   
4. Hedera Network:
   - Transaction submitted to testnet
   - Smart contract executes
   - Rent held in escrow
   - Transaction receipt returned

5. API Response:
   {
       "success": true,
       "transaction_id": "0.0.1234@1234567890.123456789",
       "contract_id": "0.0.5678",
       "amount": 10.0,
       "status": "completed"
   }

6. Frontend Confirmation:
   - Display success message
   - Show transaction details
   - Update payment status
   - Store receipt on user device
"""

# ============================================================================
# PART 9: TESTING THE INTEGRATION
# ============================================================================

"""
Run integration tests:

from backend.hedera_contract_deployment import HederaContractDeployer
from backend.hedera_contract_executor import HederaContractExecutor

# Test 1: Deployment
deployer = HederaContractDeployer()
contract_id = deployer.deploy_contract(
    'TestContract',
    bytecode_hex,
    gas=2_000_000
)
print(f"Deployed: {contract_id}")

# Test 2: Function Execution
executor = HederaContractExecutor()
params = ContractFunctionParameters()
params.add_uint256(100)

executor.execute_payable_function(
    contract_id=str(contract_id),
    function_name="testFunction",
    amount_hbar=0.1,
    params=params
)

# Test 3: State Query
result = executor.call_contract_function(
    contract_id=str(contract_id),
    function_name="getState"
)
print(f"State: {result}")

executor.close()
"""

# ============================================================================
# PART 10: TROUBLESHOOTING
# ============================================================================

"""
Common Issues and Solutions:

1. "Client not initialized"
   - Check HEDERA_ACCOUNT_ID is set
   - Check HEDERA_PRIVATE_KEY is set
   - Ensure Java 17+ is in PATH

2. "Out of gas"
   - Increase gas parameter
   - Example: gas=5_000_000 instead of 2_000_000

3. "Insufficient balance"
   - Account needs HBAR for:
     - Transaction fee (~0.001 HBAR per tx)
     - Payable amount (specified in function call)
   - Get testnet HBAR: https://portal.hedera.com

4. "Contract not found"
   - Verify contract_id format: 0.0.xxxxx
   - Check contract was successfully deployed
   - Confirm contract_id in .env is correct

5. "Function not found"
   - Verify function name matches smart contract
   - Check function signature matches
   - Ensure contract ABI is correct
"""

print(__doc__)
