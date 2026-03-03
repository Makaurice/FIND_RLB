from django.core.cache import cache
from datetime import timedelta
import os
import secrets
from typing import Dict, Any

from backend.hedera_integration_v2 import get_hedera_client

# cryptography for ED25519 signature verification
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except Exception:
    CRYPTO_AVAILABLE = False

CHALLENGE_TTL = int(os.getenv('HEDERA_CHALLENGE_TTL', 300))  # seconds


def generate_challenge(account_id: str) -> Dict[str, Any]:
    """Generate and store a random challenge (nonce) for the Hedera account.

    Returns: {'challenge': hexstring}
    """
    nonce = secrets.token_hex(32)
    cache_key = f"hedera_challenge:{account_id}"
    cache.set(cache_key, nonce, timeout=CHALLENGE_TTL)
    return {'challenge': nonce}


def _get_stored_challenge(account_id: str):
    return cache.get(f"hedera_challenge:{account_id}")


def verify_signature(account_id: str, signature_hex: str) -> Dict[str, Any]:
    """Verify a hex signature over the stored challenge for account_id.

    Returns dict with keys: success (bool) and message.
    """
    if not CRYPTO_AVAILABLE:
        return {'success': False, 'message': 'cryptography dependency not available'}

    challenge = _get_stored_challenge(account_id)
    if not challenge:
        return {'success': False, 'message': 'No challenge found or expired'}

    # fetch public key from Hedera
    hedera = get_hedera_client()
    res = hedera.get_account_public_key(account_id)
    if res.get('status') != 'SUCCESS' and res.get('status') != 'MOCK':
        return {'success': False, 'message': 'Could not fetch public key: ' + str(res.get('error'))}

    pubkey_raw = res.get('publicKey')
    if not pubkey_raw:
        return {'success': False, 'message': 'No public key available for account'}

    # Try to normalize the public key to raw bytes
    try:
        # strip 0x prefix if present
        pk = pubkey_raw
        if pk.startswith('0x'):
            pk = pk[2:]
        # If contains non-hex characters, fail
        pub_bytes = bytes.fromhex(pk)
    except Exception:
        # fallback: attempt to parse as raw string - unsupported
        return {'success': False, 'message': 'Unsupported public key format'}

    try:
        public_key = Ed25519PublicKey.from_public_bytes(pub_bytes)
    except Exception:
        return {'success': False, 'message': 'Failed to construct Ed25519 public key from bytes'}

    try:
        sig = bytes.fromhex(signature_hex)
    except Exception:
        return {'success': False, 'message': 'Signature is not valid hex'}

    try:
        public_key.verify(sig, challenge.encode('utf-8'))
        # verification succeeded
        # consume challenge
        cache.delete(f"hedera_challenge:{account_id}")
        return {'success': True, 'message': 'Verified'}
    except Exception as e:
        return {'success': False, 'message': f'Verification failed: {e}'}
