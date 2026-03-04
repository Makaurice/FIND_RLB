#!/usr/bin/env python3
"""
FIND-RLB Comprehensive Deployment Test & Verification
Tests all modules to ensure proper deployment and functionality
Date: March 4, 2026
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

class DeploymentTester:
    """Comprehensive tester for deployed FIND-RLB system"""
    
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent
        self.backend_dir = self.root_dir / 'backend'
        self.test_results = {}
        self.passed = 0
        self.failed = 0
        
    def log_test(self, test_name: str, status: bool, message: str = "", data: Dict = None):
        """Log test result"""
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}: {message}")
        
        self.test_results[test_name] = {
            'status': status,
            'message': message,
            'data': data or {},
            'timestamp': datetime.now().isoformat()
        }
        
        if status:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_environment_setup(self) -> bool:
        """Test 1: Environment Configuration"""
        print("\n" + "="*60)
        print("TEST 1: ENVIRONMENT SETUP")
        print("="*60)
        
        # Check .env file
        env_file = self.root_dir / '.env'
        if env_file.exists():
            self.log_test(".env File", True, "Found")
            
            # Load and verify environment
            from dotenv import load_dotenv
            load_dotenv(env_file)
            
            account_id = os.getenv('HEDERA_ACCOUNT_ID')
            private_key = os.getenv('HEDERA_PRIVATE_KEY')
            network = os.getenv('HEDERA_NETWORK', 'testnet')
            
            if account_id:
                self.log_test("HEDERA_ACCOUNT_ID", True, f"Set to {account_id}")
            else:
                self.log_test("HEDERA_ACCOUNT_ID", False, "Not configured")
                
            if private_key:
                masked_key = private_key[:10] + "..." + private_key[-4:]
                self.log_test("HEDERA_PRIVATE_KEY", True, f"Set ({masked_key})")
            else:
                self.log_test("HEDERA_PRIVATE_KEY", False, "Not configured")
                
            self.log_test("HEDERA_NETWORK", True, f"Set to {network}")
            
            return True
        else:
            self.log_test(".env File", False, "Not found")
            return False
    
    def test_python_imports(self) -> bool:
        """Test 2: Critical Python Imports"""
        print("\n" + "="*60)
        print("TEST 2: CRITICAL PYTHON IMPORTS")
        print("="*60)
        
        os.chdir(self.backend_dir)
        sys.path.insert(0, str(self.backend_dir))
        sys.path.insert(0, str(self.root_dir))
        
        test_imports = {
            'django': 'Django Framework',
            'rest_framework': 'Django REST Framework',
            'web3': 'Web3 Library',
            'dotenv': 'Python-dotenv',
            'cryptography': 'Cryptography',
        }
        
        all_passed = True
        for module_name, display_name in test_imports.items():
            try:
                __import__(module_name)
                self.log_test(f"Import {display_name}", True, "Available")
            except ImportError as e:
                self.log_test(f"Import {display_name}", False, str(e))
                all_passed = False
        
        return all_passed
    
    def test_hedera_client(self) -> bool:
        """Test 3: Hedera Client Initialization"""
        print("\n" + "="*60)
        print("TEST 3: HEDERA CLIENT INITIALIZATION")
        print("="*60)
        
        os.chdir(self.backend_dir)
        sys.path.insert(0, str(self.backend_dir))
        
        try:
            from hedera_integration_v2 import HederaClient
            
            # Initialize client
            hedera = HederaClient(network='testnet')
            self.log_test("Hedera Client Init", True, "Initialized successfully")
            
            if hedera.client:
                self.log_test("Hedera Network Connection", True, f"Connected to testnet as {hedera.account_id}")
            else:
                self.log_test("Hedera Network Connection", False, "Client not fully initialized (SDK may not be fully installed)")
            
            return True
        except Exception as e:
            self.log_test("Hedera Client Init", False, str(e))
            return False
    
    def test_database_models(self) -> bool:
        """Test 4: Database & Django Models"""
        print("\n" + "="*60)
        print("TEST 4: DATABASE & DJANGO MODELS")
        print("="*60)
        
        os.chdir(self.backend_dir)
        sys.path.insert(0, str(self.backend_dir))
        
        try:
            import django
            from django.conf import settings
            
            # Check Django settings
            if not settings.configured:
                os.environ['DJANGO_SETTINGS_MODULE'] = 'findrlb_django.settings'
                django.setup()
            
            self.log_test("Django Setup", True, "Configured")
            
            # Check database
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.log_test("Database Connection", True, "Connected")
            
            return True
        except Exception as e:
            self.log_test("Django Setup", False, str(e)[:100])
            return False
    
    def test_ai_modules(self) -> bool:
        """Test 5: AI Agent Modules"""
        print("\n" + "="*60)
        print("TEST 5: AI AGENT MODULES")
        print("="*60)
        
        os.chdir(self.backend_dir)
        sys.path.insert(0, str(self.root_dir / 'ai_agents'))
        
        agent_modules = {
            'matching_engine': 'Matching Engine',
            'landlord_agent': 'Landlord Agent',
            'tenant_agent': 'Tenant Agent',
            'p2p_community_agent': 'P2P Community Agent',
            'savings_to_own_agent': 'Savings-to-Own Agent',
        }
        
        all_passed = True
        for module_name, display_name in agent_modules.items():
            try:
                module = __import__(module_name)
                self.log_test(f"Module {display_name}", True, "Importable")
            except Exception as e:
                self.log_test(f"Module {display_name}", False, str(e)[:80])
                all_passed = False
        
        return all_passed
    
    def test_blockchain_contracts(self) -> bool:
        """Test 6: Smart Contracts"""
        print("\n" + "="*60)
        print("TEST 6: SMART CONTRACTS")
        print("="*60)
        
        contracts_dir = self.root_dir / 'contracts'
        contracts = ['PropertyNFT.sol', 'LeaseAgreement.sol', 'RentEscrow.sol', 'Reputation.sol', 'SavingsVault.sol']
        
        all_found = True
        for contract in contracts:
            contract_path = contracts_dir / contract
            if contract_path.exists():
                size = contract_path.stat().st_size
                self.log_test(f"Contract {contract}", True, f"Found ({size} bytes)")
            else:
                self.log_test(f"Contract {contract}", False, "Not found")
                all_found = False
        
        return all_found
    
    def test_api_endpoints(self) -> bool:
        """Test 7: API Endpoints Configuration"""
        print("\n" + "="*60)
        print("TEST 7: API ENDPOINTS CONFIGURATION")
        print("="*60)
        
        os.chdir(self.backend_dir)
        sys.path.insert(0, str(self.backend_dir))
        
        try:
            # Check main API file
            api_file = self.backend_dir / 'ai_agent_api.py'
            if api_file.exists():
                self.log_test("AI Agent API", True, "Found")
            else:
                self.log_test("AI Agent API", False, "Not found")
            
            # Check Hedera API
            hedera_api = self.backend_dir / 'hedera_integration_v2.py'
            if hedera_api.exists():
                self.log_test("Hedera Integration API", True, "Found")
            else:
                self.log_test("Hedera Integration API", False, "Not found")
            
            return True
        except Exception as e:
            self.log_test("API Configuration", False, str(e))
            return False
    
    def test_frontend_setup(self) -> bool:
        """Test 8: Frontend Configuration"""
        print("\n" + "="*60)
        print("TEST 8: FRONTEND SETUP")
        print("="*60)
        
        frontend_dir = self.root_dir / 'frontend'
        
        files_to_check = {
            'next.config.js': 'Next.js Config',
            'tsconfig.json': 'TypeScript Config',
            'package.json': 'Dependencies'
        }
        
        all_found = True
        for filename, display_name in files_to_check.items():
            path = frontend_dir / filename
            if path.exists():
                self.log_test(display_name, True, "Configured")
            else:
                self.log_test(display_name, False, "Not found")
                all_found = False
        
        return all_found
    
    def test_permissions_and_security(self) -> bool:
        """Test 9: Permissions and Security"""
        print("\n" + "="*60)
        print("TEST 9: PERMISSIONS & SECURITY")
        print("="*60)
        
        # Check .env file permissions (should not be publicly readable)
        env_file = self.root_dir / '.env'
        if env_file.exists():
            # On Windows, we can't easily check Unix permissions, so we just verify it's not in git
            gitignore = self.root_dir / '.gitignore'
            if gitignore.exists():
                gitignore_content = gitignore.read_text()
                if '.env' in gitignore_content:
                    self.log_test(".env in .gitignore", True, "Protected from version control")
                else:
                    self.log_test(".env in .gitignore", False, "Should be added to .gitignore")
            else:
                self.log_test(".env in .gitignore", False, ".gitignore not found")
        
        return True
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests"""
        print("\n" + "#"*60)
        print("# FIND-RLB DEPLOYMENT VERIFICATION SUITE")
        print("# Testing all modules for proper deployment")
        print(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("#"*60)
        
        tests = [
            self.test_environment_setup,
            self.test_python_imports,
            self.test_hedera_client,
            self.test_database_models,
            self.test_ai_modules,
            self.test_blockchain_contracts,
            self.test_api_endpoints,
            self.test_frontend_setup,
            self.test_permissions_and_security,
        ]
        
        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"⚠️  Test {test_func.__name__} encountered an error: {str(e)[:100]}")
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Success Rate: {self.passed}/{self.passed + self.failed} ({100*self.passed//(self.passed+self.failed) if (self.passed+self.failed) > 0 else 0}%)")
        print("="*60)
        
        # Save results
        summary = {
            'passed': self.passed,
            'failed': self.failed,
            'total': self.passed + self.failed,
            'timestamp': datetime.now().isoformat(),
            'results': self.test_results
        }
        
        results_file = self.root_dir / 'test_results.json'
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Results saved to: {results_file}")
        
        return summary

if __name__ == '__main__':
    tester = DeploymentTester()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if summary['failed'] == 0 else 1)
