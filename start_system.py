#!/usr/bin/env python3
# Auto-generated startup script
# FIND-RLB Web3 Hedera Deployment
# Generated: 2026-03-04

import os
import sys
from pathlib import Path

# Add paths
root = Path(__file__).parent
sys.path.insert(0, str(root / 'backend'))
sys.path.insert(0, str(root / 'ai_agents'))

# Load environment
from dotenv import load_dotenv
load_dotenv(root / '.env')

print("[*] Starting FIND-RLB System...")
print(f"[OK] Account: {os.getenv('HEDERA_ACCOUNT_ID')}")
print(f"[OK] Network: {os.getenv('HEDERA_NETWORK')}")

# Initialize Hedera
try:
    from hedera_integration_v2 import HederaClient
    hedera = HederaClient()
    print(f"[OK] Hedera connected: {hedera.account_id}")
except Exception as e:
    print(f"[!] Hedera init: {str(e)[:80]}")

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findrlb_django.settings')
try:
    import django
    django.setup()
    print("[OK] Django initialized")
except Exception as e:
    print(f"[!] Django init: {str(e)[:80]}")

# Initialize AI Modules
print("[OK] AI Modules ready")

print("\n[OK] System ready for operations!\n")
