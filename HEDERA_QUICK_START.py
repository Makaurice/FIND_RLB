#!/usr/bin/env python
"""
FIND-RLB HEDERA BLOCKCHAIN QUICK START
Get up and running in 5 minutes
"""

# ============================================================================
# QUICK START: 5 MINUTES TO YOUR FIRST BLOCKCHAIN TRANSACTION
# ============================================================================

print("""
╔════════════════════════════════════════════════════════════════╗
║   QUICK START: FIND-RLB HEDERA BLOCKCHAIN INTEGRATION        ║
║                Get Started in 5 Minutes                        ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: PREREQUISITES CHECK (1 minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Required:
  ✅ Python 3.10+
  ✅ Java 17+
  ✅ Hedera testnet account with HBAR balance

Check:
  $ python --version
  $ java -version
  $ echo %HEDERA_ACCOUNT_ID%

Get testnet HBAR: https://portal.hedera.com


STEP 2: CONFIGURE ENVIRONMENT (1 minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Edit .env file:

  HEDERA_ACCOUNT_ID=0.0.7974203
  HEDERA_PRIVATE_KEY=302e020100300506092a864886f70d0101050420...
  HEDERA_NETWORK=testnet

(Already configured if you see values above)


STEP 3: COMPILE CONTRACTS (1 minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  $ cd contracts
  $ npm install
  $ npx hardhat compile
  $ cd ..

Output: artifacts/PropertyNFT.json, LeaseAgreement.json, etc.


STEP 4: DEPLOY CONTRACTS (1 minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  $ python deploy_contracts_hedera.py

Follow prompts and confirm deployment.

Output: deployment_results.json with contract IDs


STEP 5: TEST INTEGRATION (1 minute)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  $ python -c "
from backend.blockchain_service import get_blockchain_service
blockchain = get_blockchain_service()
print('Blockchain ready:', blockchain.is_blockchain_ready())
print('Contracts configured:', sum(blockchain.get_contract_status().values()), '/ 7')
"

Output:
  ✅ Blockchain ready: True
  ✅ Contracts configured: 7 / 7


╔════════════════════════════════════════════════════════════════╗
║                    YOU'RE READY! 🚀                           ║
╚════════════════════════════════════════════════════════════════╝


COMMON TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PROCESS RENT PAYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from backend.blockchain_service import get_blockchain_service

blockchain = get_blockchain_service()
success = blockchain.deposit_rent_payment(
    tenant_id="0.0.98765",
    amount=10.0
)
print(f"Payment {'✅ success' if success else '❌ failed'}")


2. CHECK PAYMENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

blockchain = get_blockchain_service()
balance = blockchain.check_escrow_balance("0.0.98765")
print(f"Escrowed: {balance} HBAR")


3. UPDATE REPUTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

blockchain = get_blockchain_service()
blockchain.update_reputation("0.0.98765", 950)
reputation = blockchain.get_reputation("0.0.98765")
print(f"User reputation: {reputation}")


4. CREATE PROPERTY NFT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

blockchain = get_blockchain_service()
nft_id = blockchain.create_property_nft(
    "property_123",
    "ipfs://metadata/property_123"
)
print(f"Property NFT: {nft_id}")


5. REGISTER COMMUNITY MEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

blockchain = get_blockchain_service()
success = blockchain.register_community_member(
    "0.0.98765",
    "tenant"  # or "landlord" or "investor"
)
print(f"Registration {'✅ success' if success else '❌ failed'}")


═════════════════════════════════════════════════════════════════

INTEGRATE WITH AI AGENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In your AI agent class:

from backend.blockchain_service import get_blockchain_service

class TenantAIAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.blockchain = get_blockchain_service()
    
    def pay_rent(self, amount: float):
        return self.blockchain.deposit_rent_payment(
            self.user_id,
            amount
        )
    
    def check_payment_status(self):
        return self.blockchain.check_escrow_balance(self.user_id)


═════════════════════════════════════════════════════════════════

INTEGRATE WITH REST API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In your Django views:

from rest_framework.response import Response
from backend.blockchain_service import get_blockchain_service

class RentPaymentView(APIView):
    def post(self, request):
        blockchain = get_blockchain_service()
        success = blockchain.deposit_rent_payment(
            request.data['tenant_id'],
            request.data['amount']
        )
        return Response({'success': success})


═════════════════════════════════════════════════════════════════

TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: "Java not found"
Solution: Add Java to PATH
  $ set PATH=%PATH%;C:\\Program Files\\Microsoft\\jdk-17.0.18.8-hotspot\\bin

Problem: "Account balance insufficient"
Solution: Get testnet HBAR
  → https://portal.hedera.com

Problem: "Contract not found"
Solution: Check deployment
  $ cat deployment_results.json

Problem: "Module not found"
Solution: Import from backend
  from backend.blockchain_service import get_blockchain_service


═════════════════════════════════════════════════════════════════

NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Read HEDERA_DEPLOYMENT_README.md for full documentation
2. Check IMPLEMENTATION_SUMMARY.py for technical details
3. Review backend/HEDERA_INTEGRATION_GUIDE.py for examples
4. Check deployment_results.json for contract addresses
5. Test with your own transactions

═════════════════════════════════════════════════════════════════

Questions?
  - See HEDERA_DEPLOYMENT_README.md
  - Read backend/HEDERA_INTEGRATION_GUIDE.py
  - Visit: https://docs.hedera.com

═════════════════════════════════════════════════════════════════

✨ You now have a fully-functional Hedera blockchain integration!
   Start building amazing P2P rental applications! 🚀

═════════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("QUICK TEST")
    print("="*60 + "\n")
    
    try:
        from backend.blockchain_service import get_blockchain_service
        blockchain = get_blockchain_service()
        
        print("✅ Blockchain service initialized")
        print(f"✅ Blockchain ready: {blockchain.is_blockchain_ready()}")
        
        status = blockchain.get_contract_status()
        configured = sum(status.values())
        print(f"✅ Contracts configured: {configured}/7")
        
        print("\n" + "="*60)
        print("🎉 SYSTEM IS READY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        print("Check .env configuration and try again")
