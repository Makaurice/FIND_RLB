#!/usr/bin/env python3
"""
Test script for Customer Care Agent
"""

import os
import sys
import django
sys.path.append('backend')

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findrlb_django.settings')
django.setup()

# Set dummy API key for testing
os.environ['OPENAI_API_KEY'] = 'dummy_key'

try:
    from ai_agents.customer_care_agent import CustomerCareAgent
    print("✅ CustomerCareAgent imported successfully")

    # Test instantiation
    agent = CustomerCareAgent("test_user")
    print("✅ CustomerCareAgent instantiated successfully")

    # Test basic functionality (without OpenAI)
    result = agent.process_message("When is my rent due?")
    print("✅ process_message executed")
    print(f"Response: {result['response']}")
    print(f"Intent: {result['intent']}")
    print(f"Actions: {result['actions_taken']}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()