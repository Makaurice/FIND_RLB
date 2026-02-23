from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.contracts import get_contract
from django.conf import settings
from web3 import Web3

class TokenBalanceView(APIView):
    def get(self, request, address):
        contract = get_contract('FindToken')
        balance = contract.functions.balanceOf(Web3.toChecksumAddress(address)).call()
        return Response({'address': address, 'balance': balance}, status=status.HTTP_200_OK)

class TokenTransferView(APIView):
    def post(self, request):
        contract = get_contract('FindToken')
        from_addr = request.data.get('from')
        to_addr = request.data.get('to')
        amount = int(request.data.get('amount'))
        # TODO: Sign and send transaction with private key
        # tx = contract.functions.transfer(to_addr, amount).buildTransaction({...})
        return Response({'message': 'Transfer simulated'}, status=status.HTTP_200_OK)

class TokenClaimTeamView(APIView):
    def post(self, request):
        contract = get_contract('FindToken')
        # TODO: Sign and send claimTeamTokens transaction
        return Response({'message': 'Team claim simulated'}, status=status.HTTP_200_OK)
