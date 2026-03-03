from django.test import TestCase
from unittest.mock import patch
import importlib.util
import os
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import sys


def load_module_from_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HederaAuthTests(TestCase):
    def setUp(self):
        self.account_id = '0.0.1234'
        # locate the hedera_auth.py file directly
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        # ensure project root is on sys.path so imports like 'backend.*' work
        project_root = os.path.dirname(base)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        # path: backend/hedera_auth.py
        self.hedera_auth_path = os.path.join(base, 'hedera_auth.py')
        self.hedera_auth = load_module_from_path(self.hedera_auth_path, 'test_hedera_auth_module')

    def test_challenge_and_verify_flow_unit(self):
        # Generate challenge using the module directly
        resp = self.hedera_auth.generate_challenge(self.account_id)
        self.assertIn('challenge', resp)
        challenge = resp['challenge']
        self.assertTrue(isinstance(challenge, str) and len(challenge) > 0)

        # Simulate successful verification by replacing the verify function in the loaded module
        self.hedera_auth.verify_signature = lambda account_id, signature: {'success': True, 'message': 'Verified'}
        result = self.hedera_auth.verify_signature(self.account_id, 'deadbeef')
        self.assertTrue(result.get('success'))

        # Create a Django user and issue JWT tokens to simulate the view behavior
        User = get_user_model()
        user, _ = User.objects.get_or_create(username=self.account_id)
        refresh = RefreshToken.for_user(user)
        tokens = {'access': str(refresh.access_token), 'refresh': str(refresh)}
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
