# contracts.py - Backend integration for all Hedera/Ethereum contracts
from web3 import Web3
from django.conf import settings
from backend.hedera_integration import HederaClient

# Replace with actual ABIs and deployed addresses/IDs after deployment
CONTRACTS = {
    'PropertyNFT': {
        'abi': [...],
        'address': '0xPropertyNFT...',
        'hedera_id': getattr(settings, 'HEDERA_PROPERTYNFT_CONTRACT_ID', None),
    },
    'LeaseAgreement': {
        'abi': [...],
        'address': '0xLeaseAgreement...',
        'hedera_id': getattr(settings, 'HEDERA_LEASEAGREEMENT_CONTRACT_ID', None),
    },
    'RentEscrow': {
        'abi': [...],
        'address': '0xRentEscrow...',
        'hedera_id': getattr(settings, 'HEDERA_RENTESCROW_CONTRACT_ID', None),
    },
    'SavingsVault': {
        'abi': [...],
        'address': '0xSavingsVault...',
        'hedera_id': getattr(settings, 'HEDERA_SAVINGSVAULT_CONTRACT_ID', None),
    },
    'ThirdPartyPayment': {
        'abi': [...],
        'address': '0xThirdPartyPayment...',
        'hedera_id': getattr(settings, 'HEDERA_THIRDPARTYPAYMENT_CONTRACT_ID', None),
    },
    'Reputation': {
        'abi': [...],
        'address': '0xReputation...',
        'hedera_id': getattr(settings, 'HEDERA_REPUTATION_CONTRACT_ID', None),
    },
    'P2PCommunity': {
        'abi': [...],
        'address': '0xP2PCommunity...',
        'hedera_id': getattr(settings, 'HEDERA_P2PCOMMUNITY_CONTRACT_ID', None),
    },
    'MovingService': {
        'abi': [...],
        'address': '0xMovingService...',
        'hedera_id': getattr(settings, 'HEDERA_MOVINGSERVICE_CONTRACT_ID', None),
    },
}

# initialize web3 provider (HTTP or WS) from Django settings
w3 = Web3(Web3.HTTPProvider(getattr(settings, 'WEB3_PROVIDER_URL', 'http://localhost:8545')))

# hedra client for on-chain functionality
hedera = HederaClient(
    account_id=getattr(settings, 'HEDERA_ACCOUNT_ID', None),
    private_key=getattr(settings, 'HEDERA_PRIVATE_KEY', None),
    network=getattr(settings, 'HEDERA_NETWORK', 'testnet'),
)

# optional: check web3 connection
if w3 and not w3.isConnected():
    # logging could be added here
    pass


def get_contract(name):
    """Return a web3 contract or raise if unsupported."""
    info = CONTRACTS.get(name)
    if info is None:
        raise ValueError(f"contract '{name}' is not configured")
    if w3 and w3.isConnected():
        return w3.eth.contract(address=info['address'], abi=info['abi'])
    else:
        raise RuntimeError("Web3 provider not available")


def call_hedera_contract(name: str, function: str, params: list = None, gas: int = 100000) -> dict:
    """Invoke a function on an on-chain Hedera contract by name.

    This helper converts a named contract into its deployed ID, then calls
    ``hedera.call_contract``.  The caller is responsible for providing
    correct parameter formatting according to the ABI.
    """
    info = CONTRACTS.get(name)
    if not info or not info.get('hedera_id'):
        raise ValueError(f"Hedera contract '{name}' not configured or has no id")
    return hedera.call_contract(info['hedera_id'], function, params or [], gas)

# Example usage for PropertyNFT
# contract = get_contract('PropertyNFT')
# tx = contract.functions.registerProperty(...).buildTransaction({...})
# hedera.call_contract(CONTRACTS['PropertyNFT']['hedera_id'], 'registerProperty', [...])

# Example usage for PropertyNFT
# contract = get_contract('PropertyNFT')
# tx = contract.functions.registerProperty(...).buildTransaction({...})
