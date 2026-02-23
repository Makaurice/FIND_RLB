# contracts.py - Backend integration for all Hedera contracts
from web3 import Web3
from django.conf import settings

# Replace with actual ABIs and deployed addresses after deployment
CONTRACTS = {
    'PropertyNFT': {
        'abi': [...],
        'address': '0xPropertyNFT...'
    },
    'LeaseAgreement': {
        'abi': [...],
        'address': '0xLeaseAgreement...'
    },
    'RentEscrow': {
        'abi': [...],
        'address': '0xRentEscrow...'
    },
    'SavingsVault': {
        'abi': [...],
        'address': '0xSavingsVault...'
    },
    'ThirdPartyPayment': {
        'abi': [...],
        'address': '0xThirdPartyPayment...'
    },
    'Reputation': {
        'abi': [...],
        'address': '0xReputation...'
    },
}

w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))

def get_contract(name):
    info = CONTRACTS[name]
    return w3.eth.contract(address=info['address'], abi=info['abi'])

# Example usage for PropertyNFT
# contract = get_contract('PropertyNFT')
# tx = contract.functions.registerProperty(...).buildTransaction({...})
