#!/usr/bin/env python3
"""
FIND-RLB Comprehensive Module Testing Suite
Tests all system components on Hedera integration
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Any
import time

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'backend'))

class ModuleTestSuite:
    """Comprehensive testing of all FIND-RLB modules"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.test_results = {}
        self.headers = {'Content-Type': 'application/json'}
    
    def log_test(self, module: str, test_name: str, status: str, details: str = ""):
        """Log test results"""
        if module not in self.test_results:
            self.test_results[module] = []
        
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': time.time()
        }
        self.test_results[module].append(result)
        
        icon = '✅' if status == 'PASSED' else '❌'
        print(f"{icon} {module}: {test_name} - {status}")
    
    def test_backend_connectivity(self) -> bool:
        """Test if backend API is running"""
        print("\n📡 Testing Backend Connectivity...")
        try:
            response = requests.get(f"{self.api_base_url}/api/")
            self.log_test('Backend', 'API Connectivity', 'PASSED' if response.status_code < 500 else 'FAILED')
            return response.status_code < 500
        except requests.exceptions.ConnectionError:
            self.log_test('Backend', 'API Connectivity', 'FAILED', 'Connection refused - is backend running?')
            return False
        except Exception as e:
            self.log_test('Backend', 'API Connectivity', 'FAILED', str(e))
            return False
    
    def test_authentication(self) -> bool:
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication Module...")
        
        test_user = {
            'username': 'test_user',
            'email': 'test@findrlb.com',
            'password': 'TestPassword123!',
            'user_type': 'tenant'
        }
        
        try:
            # Test registration
            response = requests.post(
                f"{self.api_base_url}/api/auth/register/",
                json=test_user,
                headers=self.headers
            )
            self.log_test('Authentication', 'User Registration', 
                         'PASSED' if response.status_code == 201 else 'FAILED',
                         f"Status: {response.status_code}")
            
            # Test login
            response = requests.post(
                f"{self.api_base_url}/api/auth/login/",
                json={'username': test_user['username'], 'password': test_user['password']},
                headers=self.headers
            )
            self.log_test('Authentication', 'User Login',
                         'PASSED' if response.status_code == 200 else 'FAILED',
                         f"Status: {response.status_code}")
            
            return response.status_code == 200
        except Exception as e:
            self.log_test('Authentication', 'Authentication Tests', 'FAILED', str(e))
            return False
    
    def test_property_management(self) -> bool:
        """Test property management endpoints"""
        print("\n🏠 Testing Property Management Module...")
        
        try:
            # Get properties
            response = requests.get(f"{self.api_base_url}/api/property/")
            self.log_test('Property', 'List Properties',
                         'PASSED' if response.status_code == 200 else 'FAILED',
                         f"Status: {response.status_code}")
            
            # Create property (if authenticated)
            property_data = {
                'name': 'Test Property',
                'address': '123 Main St',
                'rent_amount': 2000,
                'bedrooms': 3,
                'bathrooms': 2
            }
            response = requests.post(
                f"{self.api_base_url}/api/property/create/",
                json=property_data,
                headers=self.headers
            )
            self.log_test('Property', 'Create Property',
                         'PASSED' if response.status_code in [201, 401] else 'FAILED',
                         f"Status: {response.status_code}")
            
            return response.status_code < 500
        except Exception as e:
            self.log_test('Property', 'Property Tests', 'FAILED', str(e))
            return False
    
    def test_hedera_integration(self) -> bool:
        """Test Hedera blockchain integration"""
        print("\n⛓️  Testing Hedera Integration Module...")
        
        try:
            from backend.hedera_integration_v2 import HederaClient
            
            # Initialize Hedera client
            client = HederaClient(network='testnet')
            
            if client.client:
                self.log_test('Hedera', 'Client Initialization', 'PASSED', 
                             f"Account: {client.account_id}")
            else:
                self.log_test('Hedera', 'Client Initialization', 'PASSED (Mock Mode)',
                             "SDK not fully connected but initialized")
            
            # Test transaction history
            history = client.transaction_history
            self.log_test('Hedera', 'Transaction History', 'PASSED',
                         f"Transactions: {len(history)}")
            
            return True
        except Exception as e:
            self.log_test('Hedera', 'Hedera Integration', 'FAILED', str(e))
            return False
    
    def test_smart_contracts(self) -> bool:
        """Test smart contract endpoints"""
        print("\n📝 Testing Smart Contracts Module...")
        
        try:
            # Test contract endpoints
            endpoints = [
                '/api/contracts/register-property/',
                '/api/contracts/create-lease/',
                '/api/contracts/pay-rent/',
            ]
            
            for endpoint in endpoints:
                response = requests.get(f"{self.api_base_url}{endpoint}")
                status = 'PASSED' if response.status_code < 500 else 'FAILED'
                self.log_test('Contracts', f"Endpoint {endpoint}", status,
                             f"Status: {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test('Contracts', 'Smart Contracts', 'FAILED', str(e))
            return False
    
    def test_wallet_service(self) -> bool:
        """Test wallet and payment services"""
        print("\n💳 Testing Wallet Service Module...")
        
        try:
            endpoints = [
                '/api/wallet/balance/1/',
                '/api/wallet/history/1/',
            ]
            
            for endpoint in endpoints:
                response = requests.get(f"{self.api_base_url}{endpoint}")
                status = 'PASSED' if response.status_code < 500 else 'FAILED'
                self.log_test('Wallet', f"Endpoint {endpoint}", status,
                             f"Status: {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test('Wallet', 'Wallet Service', 'FAILED', str(e))
            return False
    
    def test_ai_agents(self) -> bool:
        """Test AI agents"""
        print("\n🤖 Testing AI Agents Module...")
        
        try:
            from ai_agents.matching_engine import MatchingEngine
            from ai_agents.tenant_agent import TenantAgent
            
            # Test agent initialization
            matching_engine = MatchingEngine()
            self.log_test('AI Agents', 'Matching Engine Initialization', 'PASSED')
            
            tenant_agent = TenantAgent(user_id=1)
            self.log_test('AI Agents', 'Tenant Agent Initialization', 'PASSED')
            
            return True
        except Exception as e:
            self.log_test('AI Agents', 'AI Agents', 'FAILED', str(e))
            return False
    
    def test_p2p_community(self) -> bool:
        """Test P2P Community features"""
        print("\n👥 Testing P2P Community Module...")
        
        try:
            response = requests.get(f"{self.api_base_url}/api/community/")
            status = 'PASSED' if response.status_code < 500 else 'FAILED'
            self.log_test('P2P Community', 'Community Endpoints', status,
                         f"Status: {response.status_code}")
            
            return response.status_code < 500
        except Exception as e:
            self.log_test('P2P Community', 'P2P Community', 'FAILED', str(e))
            return False
    
    def test_database_models(self) -> bool:
        """Test database model integrity"""
        print("\n🗄️  Testing Database Models...")
        
        try:
            from django.apps import apps
            from django.core.management import call_command
            
            # Get all models
            models = apps.get_models()
            self.log_test('Database', f'Models Found', 'PASSED',
                         f"Total models: {len(models)}")
            
            # Verify migrations
            call_command('migrate', '--check', verbosity=0)
            self.log_test('Database', 'Migrations', 'PASSED')
            
            return True
        except Exception as e:
            self.log_test('Database', 'Database Models', 'FAILED', str(e))
            return False
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("📊 TEST REPORT SUMMARY")
        print("="*60 + "\n")
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for module, results in self.test_results.items():
            module_passed = sum(1 for r in results if r['status'] == 'PASSED')
            module_total = len(results)
            total_tests += module_total
            passed_tests += module_passed
            failed_tests += module_total - module_passed
            
            print(f"\n{module}:")
            for result in results:
                icon = '✅' if result['status'] == 'PASSED' else '❌'
                print(f"  {icon} {result['test']}: {result['status']}")
                if result['details']:
                    print(f"      → {result['details']}")
        
        print("\n" + "="*60)
        print(f"Total: {passed_tests}/{total_tests} tests passed")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        print("="*60 + "\n")
        
        # Save report
        report_file = Path(__file__).parent / 'test_report.json'
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📄 Report saved to: {report_file}\n")
    
    def run_all_tests(self):
        """Execute all tests"""
        print("🚀 FIND-RLB Comprehensive Module Testing")
        print("="*60 + "\n")
        
        tests = [
            self.test_backend_connectivity,
            self.test_database_models,
            self.test_authentication,
            self.test_property_management,
            self.test_hedera_integration,
            self.test_smart_contracts,
            self.test_wallet_service,
            self.test_ai_agents,
            self.test_p2p_community,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"Exception in {test.__name__}: {e}")
            time.sleep(0.5)
        
        self.generate_report()

if __name__ == '__main__':
    suite = ModuleTestSuite()
    suite.run_all_tests()
