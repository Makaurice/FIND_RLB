from web3 import Web3
from django.conf import settings

PROPERTY_NFT_ABI = [...]  # Replace with actual ABI
PROPERTY_NFT_ADDRESS = '0x...'  # Replace with deployed contract address

w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
contract = w3.eth.contract(address=PROPERTY_NFT_ADDRESS, abi=PROPERTY_NFT_ABI)

# Example: Register property endpoint

def register_property(owner, location, metadata_uri, for_rent, for_sale, price):
    tx = contract.functions.registerProperty(location, metadata_uri, for_rent, for_sale, price).buildTransaction({
        'from': owner,
        'nonce': w3.eth.get_transaction_count(owner)
    })
    # Sign and send transaction logic here
    return tx
