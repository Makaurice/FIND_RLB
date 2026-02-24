from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.contracts import get_contract
from django.conf import settings
from web3 import Web3
from datetime import datetime

class TokenBalanceView(APIView):
    """Get FIND token balance for an address."""
    def get(self, request, address):
        try:
            contract = get_contract('FindToken')
            # Validate address format
            try:
                checksum_addr = Web3.toChecksumAddress(address)
            except:
                return Response({'error': 'Invalid address format'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call real token contract
            # balance = contract.functions.balanceOf(checksum_addr).call()
            # For now: Return mock balance
            balance = 10000 * (10 ** 18)  # 10,000 FIND tokens
            
            return Response({
                'address': checksum_addr,
                'balance': balance,
                'balance_fmt': balance / (10 ** 18),
                'symbol': 'FIND',
                'decimals': 18,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TokenTransferView(APIView):
    """Transfer FIND tokens from one address to another."""
    def post(self, request):
        try:
            from_addr = request.data.get('from')
            to_addr = request.data.get('to')
            amount_str = request.data.get('amount')
            
            if not all([from_addr, to_addr, amount_str]):
                return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                from_addr = Web3.toChecksumAddress(from_addr)
                to_addr = Web3.toChecksumAddress(to_addr)
                amount = int(float(amount_str) * (10 ** 18))  # Convert to wei
            except:
                return Response({'error': 'Invalid address or amount format'}, status=status.HTTP_400_BAD_REQUEST)
            
            if amount <= 0:
                return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Build and sign transaction
            # contract = get_contract('FindToken')
            # tx_dict = contract.functions.transfer(to_addr, amount).buildTransaction({
            #     'from': from_addr,
            #     'gas': 200000,
            #     'gasPrice': w3.eth.gas_price,
            #     'nonce': w3.eth.get_transaction_count(from_addr),
            # })
            # signed_tx = w3.eth.account.sign_transaction(tx_dict, private_key=settings.PRIVATE_KEY)
            # tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            return Response({
                'status': 'confirmed',
                'from': from_addr,
                'to': to_addr,
                'amount': amount,
                'amount_fmt': amount / (10 ** 18),
                'transactionHash': '0x' + 'f' * 64,
                'timestamp': str(datetime.now()),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TokenClaimTeamView(APIView):
    """Claim team allocation of FIND tokens (one-time)."""
    def post(self, request):
        try:
            recipient = request.data.get('recipient')
            
            if not recipient:
                return Response({'error': 'Recipient address required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                recipient = Web3.toChecksumAddress(recipient)
            except:
                return Response({'error': 'Invalid address format'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call contract function to mint team tokens
            # contract = get_contract('FindToken')
            # team_allocation = 5000000 * (10 ** 18)  # 5M FIND for team
            # tx = contract.functions.claimTeamTokens(recipient).buildTransaction({
            #     'from': settings.ADMIN_ADDRESS,
            #     'gas': 300000,
            # })
            # Send transaction...
            
            team_allocation = 5000000 * (10 ** 18)
            return Response({
                'status': 'claimed',
                'recipient': recipient,
                'amount': team_allocation,
                'amount_fmt': team_allocation / (10 ** 18),
                'transactionHash': '0x' + 'a' * 64,
                'timestamp': str(datetime.now()),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
