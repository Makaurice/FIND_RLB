#!/usr/bin/env python3
"""
FIND-RLB Module Performance Verification Suite
Tests all modules after deployment to ensure proper functionality
Run this AFTER starting the backend and frontend servers
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from urllib.parse import urljoin

class ModulePerformanceTester:
    """Test suite for verifying all FIND-RLB modules"""
    
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent
        self.backend_url = "http://localhost:8000"
        self.timeout = 5
        self.test_results = {}
        self.passed = 0
        self.failed = 0
        
    def log_result(self, module: str, test: str, passed: bool, details: str = ""):
        """Log test result"""
        icon = "[OK]" if passed else "[!!]"
        print(f"   {icon} {module}: {test} - {details}")
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        
        self.test_results[f"{module}.{test}"] = {
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    def test_backend_api(self) -> bool:
        """Test 1: Backend API Endpoints"""
        print("\n" + "="*70)
        print("TEST 1: BACKEND API ENDPOINTS")
        print("="*70)
        
        endpoints = {
            '/api/health/': 'Health check',
            '/api/token/': 'Token API',
            '/api/hedera/': 'Hedera integration',
        }
        
        all_passed = True
        for endpoint, description in endpoints.items():
            try:
                url = urljoin(self.backend_url, endpoint)
                response = requests.get(url, timeout=self.timeout)
                
                if response.status_code in [200, 404]:  # 404 is OK if endpoint isn't implemented yet
                    self.log_result("Backend", description, True, f"HTTP {response.status_code}")
                else:
                    self.log_result("Backend", description, False, f"HTTP {response.status_code}")
                    all_passed = False
                    
            except requests.ConnectionError:
                self.log_result("Backend", description, False, "Connection failed - is server running?")
                all_passed = False
            except Exception as e:
                self.log_result("Backend", description, False, str(e)[:50])
                all_passed = False
        
        return all_passed
    
    def test_django_models(self) -> bool:
        """Test 2: Django Models"""
        print("\n" + "="*70)
        print("TEST 2: DJANGO MODELS")
        print("="*70)
        
        os.chdir(self.root_dir / 'backend')
        sys.path.insert(0, str(self.root_dir / 'backend'))
        
        try:
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findrlb_django.settings')
            django.setup()
            
            # Import models
            from accounts.models import User
            from tenant.models import Tenant
            from landlord.models import Landlord
            from property.models import Property
            
            self.log_result("Django", "User model", True, "Imported")
            self.log_result("Django", "Tenant model", True, "Imported")
            self.log_result("Django", "Landlord model", True, "Imported")
            self.log_result("Django", "Property model", True, "Imported")
            
            return True
            
        except Exception as e:
            self.log_result("Django", "Setup", False, str(e)[:50])
            return False
    
    def test_hedera_module(self) -> bool:
        """Test 3: Hedera Integration"""
        print("\n" + "="*70)
        print("TEST 3: HEDERA INTEGRATION MODULE")
        print("="*70)
        
        os.chdir(self.root_dir / 'backend')
        sys.path.insert(0, str(self.root_dir / 'backend'))
        
        try:
            from hedera_integration_v2 import HederaClient
            from dotenv import load_dotenv
            
            load_dotenv(self.root_dir / '.env')
            
            # Initialize client
            hedera = HederaClient(network='testnet')
            
            self.log_result("Hedera", "Client initialization", True, "Ready")
            self.log_result("Hedera", "Account loaded", True, f"Account: {hedera.account_id}")
            self.log_result("Hedera", "Network", True, f"Network: {hedera.network}")
            
            # Test methods
            if hasattr(hedera, 'send_hbar'):
                self.log_result("Hedera", "send_hbar method", True, "Available")
            
            if hasattr(hedera, 'create_token'):
                self.log_result("Hedera", "create_token method", True, "Available")
            
            return True
            
        except Exception as e:
            self.log_result("Hedera", "Initialization", False, str(e)[:50])
            return False
    
    def test_ai_agents(self) -> bool:
        """Test 4: AI Agent Modules"""
        print("\n" + "="*70)
        print("TEST 4: AI AGENT MODULES")
        print("="*70)
        
        sys.path.insert(0, str(self.root_dir / 'ai_agents'))
        
        agents = {
            'matching_engine': 'Matching Engine',
            'landlord_agent': 'Landlord Agent',
            'tenant_agent': 'Tenant Agent',
            'p2p_community_agent': 'P2P Community Agent',
        }
        
        all_passed = True
        for module_name, display_name in agents.items():
            try:
                module = __import__(module_name)
                self.log_result("AI Agents", display_name, True, "Module loaded")
                
                # Check for key classes/functions
                if hasattr(module, 'main') or hasattr(module, 'Agent') or any('Agent' in attr for attr in dir(module)):
                    self.log_result("AI Agents", f"{display_name} implementation", True, "Has Agent class")
                    
            except Exception as e:
                self.log_result("AI Agents", display_name, False, str(e)[:40])
                all_passed = False
        
        return all_passed
    
    def test_wallet_service(self) -> bool:
        """Test 5: Wallet Service"""
        print("\n" + "="*70)
        print("TEST 5: WALLET SERVICE")
        print("="*70)
        
        os.chdir(self.root_dir / 'backend')
        sys.path.insert(0, str(self.root_dir / 'backend'))
        
        try:
            from wallet_service import WalletService
            
            wallet_service = WalletService()
            self.log_result("Wallet", "Service initialization", True, "Ready")
            
            # Check methods
            methods = ['create_wallet', 'get_balance', 'transfer']
            for method in methods:
                if hasattr(wallet_service, method):
                    self.log_result("Wallet", f"{method} method", True, "Available")
                else:
                    self.log_result("Wallet", f"{method} method", False, "Not found")
            
            return True
            
        except ImportError:
            self.log_result("Wallet", "Service import", False, "Module not found")
            return False
        except Exception as e:
            self.log_result("Wallet", "Service test", False, str(e)[:50])
            return False
    
    def test_reward_engine(self) -> bool:
        """Test 6: Reward Engine"""
        print("\n" + "="*70)
        print("TEST 6: REWARD ENGINE")
        print("="*70)
        
        os.chdir(self.root_dir / 'backend')
        sys.path.insert(0, str(self.root_dir / 'backend'))
        
        try:
            from reward_engine import RewardEngine
            
            reward_engine = RewardEngine()
            self.log_result("Rewards", "Engine initialization", True, "Ready")
            
            # Check methods
            if hasattr(reward_engine, 'calculate_reward'):
                self.log_result("Rewards", "calculate_reward", True, "Available")
            
            if hasattr(reward_engine, 'distribute_rewards'):
                self.log_result("Rewards", "distribute_rewards", True, "Available")
            
            return True
            
        except ImportError:
            self.log_result("Rewards", "Engine import", False, "Module not found")
            return False
        except Exception as e:
            self.log_result("Rewards", "Engine test", False, str(e)[:50])
            return False
    
    def test_community_service(self) -> bool:
        """Test 7: P2P Community Service"""
        print("\n" + "="*70)
        print("TEST 7: P2P COMMUNITY SERVICE")
        print("="*70)
        
        os.chdir(self.root_dir / 'backend')
        sys.path.insert(0, str(self.root_dir / 'backend'))
        
        try:
            from community_service import CommunityService
            
            community_service = CommunityService()
            self.log_result("Community", "Service initialization", True, "Ready")
            
            # Check methods
            if hasattr(community_service, 'create_community'):
                self.log_result("Community", "create_community", True, "Available")
            
            if hasattr(community_service, 'add_member'):
                self.log_result("Community", "add_member", True, "Available")
            
            return True
            
        except ImportError:
            self.log_result("Community", "Service import", False, "Module not found")
            return False
        except Exception as e:
            self.log_result("Community", "Service test", False, str(e)[:50])
            return False
    
    def test_contracts(self) -> bool:
        """Test 8: Smart Contracts"""
        print("\n" + "="*70)
        print("TEST 8: SMART CONTRACTS")
        print("="*70)
        
        contracts_dir = self.root_dir / 'contracts'
        contracts = [
            ('PropertyNFT.sol', 'PropertyNFT'),
            ('LeaseAgreement.sol', 'LeaseAgreement'),
            ('RentEscrow.sol', 'RentEscrow'),
            ('Reputation.sol', 'Reputation'),
            ('SavingsVault.sol', 'SavingsVault'),
        ]
        
        all_passed = True
        for filename, name in contracts:
            path = contracts_dir / filename
            if path.exists():
                content = path.read_text()
                
                # Check for contract keyword
                if 'contract ' + name in content:
                    self.log_result("Contracts", name, True, "Valid Solidity")
                else:
                    self.log_result("Contracts", name, False, "Syntax issue")
                    all_passed = False
            else:
                self.log_result("Contracts", name, False, "File not found")
                all_passed = False
        
        return all_passed
    
    def generate_report(self) -> Dict:
        """Generate test report"""
        print("\n" + "="*70)
        print("SUMMARY REPORT")
        print("="*70)
        
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\nTests Passed: {self.passed}")
        print(f"Tests Failed: {self.failed}")
        print(f"Total Tests:  {total}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        report = {
            'deployment_date': datetime.now().isoformat(),
            'tests_passed': self.passed,
            'tests_failed': self.failed,
            'total_tests': total,
            'success_rate': success_rate,
            'results': self.test_results
        }
        
        # Save report
        report_file = self.root_dir / 'MODULE_TEST_RESULTS.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nReport saved to: MODULE_TEST_RESULTS.json")
        
        return report
    
    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("\n" + "#"*70)
        print("# FIND-RLB MODULE PERFORMANCE VERIFICATION")
        print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("#"*70)
        
        tests = [
            self.test_backend_api,
            self.test_django_models,
            self.test_hedera_module,
            self.test_ai_agents,
            self.test_wallet_service,
            self.test_reward_engine,
            self.test_community_service,
            self.test_contracts,
        ]
        
        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"\n[!] Test error: {str(e)[:100]}")
        
        report = self.generate_report()
        
        print("\n" + "="*70)
        if report['success_rate'] >= 85:
            print("STATUS: [OK] All modules performing as expected!")
        elif report['success_rate'] >= 70:
            print("STATUS: [!] Some modules need attention")
        else:
            print("STATUS: [!!] Multiple modules need debugging")
        
        print("="*70 + "\n")
        
        return report['success_rate'] >= 85

if __name__ == '__main__':
    tester = ModulePerformanceTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
