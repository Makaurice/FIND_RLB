#!/usr/bin/env python3
"""
FIND-RLB Quick Diagnostic - No Complex Dependencies
Simple tests that don't require problematic imports
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def test_environment():
    """Test environment variables"""
    print("\n" + "="*60)
    print("ENVIRONMENT CHECK")
    print("="*60)
    
    env_checks = {
        'HEDERA_ACCOUNT_ID': 'Hedera Account',
        'HEDERA_PRIVATE_KEY': 'Hedera Private Key',
        'HEDERA_NETWORK': 'Network (testnet/mainnet)',
        'DJANGO_SETTINGS_MODULE': 'Django Settings' ,
        'SECRET_KEY': 'Secret Key'
    }
    
    passed = 0
    for env_var, desc in env_checks.items():
        value = os.getenv(env_var)
        if value:
            masked = (value[:8] + "..." + value[-4:]) if len(value) > 12 else value
            print(f"✅ {desc}: {masked}")
            passed += 1
        else:
            print(f"⚠️  {desc}: Not set")
    
    return passed

def test_file_structure():
    """Test critical files exist"""
    print("\n" + "="*60)
    print("FILE STRUCTURE CHECK")
    print("="*60)
    
    root = Path(__file__).parent
    files_to_check = {
        'backend/.env': 'Environment file',
        'backend/hedera_integration_v2.py': 'Hedera Integration',
        'contracts/PropertyNFT.sol': 'PropertyNFT Contract',
        'frontend/package.json': 'Frontend Config',
        'ai_agents/__init__.py': 'AI Agents Module',
    }
    
    passed = 0
    for filepath, desc in files_to_check.items():
        full_path = root / filepath
        if full_path.exists():
            size = full_path.stat().st_size if full_path.is_file() else "dir"
            print(f"✅ {desc}: Found")
            passed += 1
        else:
            print(f"❌ {desc}: Missing - {filepath}")
    
    return passed

def test_directories():
    """Test critical directories"""
    print("\n" + "="*60)
    print("DIRECTORY CHECK")
    print("="*60)
    
    root = Path(__file__).parent
    dirs_to_check = {
        'backend': 'Backend',
        'frontend': 'Frontend',
        'contracts': 'Contracts',
        'ai_agents': 'AI Agents',
    }
    
    passed = 0
    for dirname, desc in dirs_to_check.items():
        dirpath = root / dirname
        if dirpath.is_dir():
            files_count = len(list(dirpath.glob('*')))
            print(f"✅ {desc}: {files_count} items")
            passed += 1
        else:
            print(f"❌ {desc}: Not found")
    
    return passed

def test_hedera_credentials():
    """Test Hedera credentials format"""
    print("\n" + "="*60)
    print("HEDERA CREDENTIALS CHECK")
    print("="*60)
    
    root = Path(__file__).parent
    env_file = root / '.env'
    
    if not env_file.exists():
        print("❌ .env file not found")
        return 0
    
    content = env_file.read_text()
    passed = 0
    
    # Check for account ID
    if 'HEDERA_ACCOUNT_ID=' in content:
        lines = [line for line in content.split('\n') if 'HEDERA_ACCOUNT_ID=' in line and not line.strip().startswith('#')]
        if lines:
            account_match = lines[0].split('=',1)[1].strip()
            if account_match.startswith('0.0.'):
                print(f"✅ Account ID format: {account_match}")
                passed += 1
            else:
                print(f"❌ Account ID format: {account_match} (should be 0.0.xxxxx)")
    else:
        print("❌ HEDERA_ACCOUNT_ID not found in .env")
    
    # Check for private key
    if 'HEDERA_PRIVATE_KEY=' in content:
        lines = [line for line in content.split('\n') if 'HEDERA_PRIVATE_KEY=' in line and not line.strip().startswith('#')]
        if lines:
            key = lines[0].split('=', 1)[1].strip()
            if len(key) == 64 or (len(key) == 66 and key.startswith('0x')):
                print(f"✅ Private Key format: {'0x' + key[:8]}...{key[-4:]} ({len(key)} chars)")
                passed += 1
            else:
                print(f"⚠️  Private Key format: {len(key)} chars (expected 64 or 66)")
    else:
        print("❌ HEDERA_PRIVATE_KEY not found in .env")
    
    return passed

def test_packages():
    """Test if key packages can be imported (safely)"""
    print("\n" + "="*60)
    print("PACKAGE CHECK (Basic)")
    print("="*60)
    
    packages = [
        ('django', 'Django'),
        ('rest_framework', 'Django REST'),
        ('dotenv', 'Python-dotenv'),
        ('cryptography', 'Cryptography'),
    ]
    
    passed = 0
    for module_name, display_name in packages:
        try:
            __import__(module_name)
            print(f"✅ {display_name}: Installed")
            passed += 1
        except ImportError:
            print(f"❌ {display_name}: Not installed")
    
    return passed

def main():
    root = Path(__file__).parent
    os.chdir(root)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv(root / '.env')
    
    print("\n" + "#"*60)
    print("# FIND-RLB QUICK DIAGNOSTIC")
    print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#"*60)
    
    results = {
        'Environment': test_environment(),
        'Files': test_file_structure(),
        'Directories': test_directories(),
        'Hedera Credentials': test_hedera_credentials(),
        'Packages': test_packages(),
    }
    
    total_passed = sum(results.values())
    total_checks = sum([
        4,  # environment
        5,  # files  
        4,  # directories
        2,  # hedera creds
        4,  # packages
    ])
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for section, passed in results.items():
        print(f"{section}: {passed}  checks passed")
    
    print(f"\n📊 Overall: {total_passed}/{total_checks} checks passed ({100*total_passed//total_checks}%)")
    print("="*60 + "\n")
    
    if total_passed >= total_checks - 2:
        print("✅ System is ready for deployment!")
        return 0
    else:
        print("⚠️  Some checks failed. Review above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
