from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from wallet_service import WalletService
from datetime import datetime

class WalletBalanceView(APIView):
    """Get user wallet balances."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user_id = request.user.id
            wallet = WalletService(str(user_id))
            balance = wallet.get_balance()
            return Response(balance, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletCreateView(APIView):
    """Create new wallet (custodial or non-custodial)."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            wallet_type = request.data.get('wallet_type', 'custodial')  # custodial or non-custodial
            wallet = WalletService(str(user_id))
            
            if wallet_type == 'non-custodial':
                result = wallet.create_non_custodial_wallet()
            else:
                result = wallet.create_custodial_wallet()
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankAccountLinkView(APIView):
    """Link bank account for deposits/withdrawals."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            bank_name = request.data.get('bank_name')
            account_number = request.data.get('account_number')
            
            if not bank_name or not account_number:
                return Response({'error': 'Bank name and account required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.link_bank_account(bank_name, account_number)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepositView(APIView):
    """Deposit funds from linked bank account."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            amount = request.data.get('amount')
            bank = request.data.get('bank')
            
            if not amount or amount <= 0 or not bank:
                return Response({'error': 'Valid amount and bank required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.deposit_from_bank(float(amount), bank)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawView(APIView):
    """Withdraw funds to linked bank account."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            amount = request.data.get('amount')
            bank = request.data.get('bank')
            
            if not amount or amount <= 0 or not bank:
                return Response({'error': 'Valid amount and bank required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.withdraw_to_bank(float(amount), bank)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransferView(APIView):
    """Transfer FIND tokens to another user."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            recipient_id = request.data.get('recipient_id')
            amount = request.data.get('amount')
            reason = request.data.get('reason', 'FIND token transfer')
            
            if not recipient_id or not amount or amount <= 0:
                return Response({'error': 'Valid recipient and amount required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.transfer_to_user(recipient_id, float(amount), reason)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EscrowLockView(APIView):
    """Lock funds in escrow."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            amount = request.data.get('amount')
            lease_id = request.data.get('lease_id')
            
            if not amount or amount <= 0 or not lease_id:
                return Response({'error': 'Valid amount and lease_id required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.lock_funds_escrow(float(amount), int(lease_id))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SavingsDepositView(APIView):
    """Deposit into savings-to-own plan."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            amount = request.data.get('amount')
            plan_id = request.data.get('plan_id')
            
            if not amount or amount <= 0 or not plan_id:
                return Response({'error': 'Valid amount and plan_id required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.deposit_savings(float(amount), int(plan_id))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionHistoryView(APIView):
    """Get wallet transaction history."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user_id = request.user.id
            limit = request.query_params.get('limit', 50)
            wallet = WalletService(str(user_id))
            result = wallet.get_transaction_history(int(limit))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentAuthorizationView(APIView):
    """Authorize automatic rent payments."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user_id = request.user.id
            lease_id = request.data.get('lease_id')
            amount = request.data.get('amount')
            auto_debit = request.data.get('auto_debit_max', 0)
            
            if not lease_id or not amount or amount <= 0:
                return Response({'error': 'Valid lease_id and amount required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet = WalletService(str(user_id))
            result = wallet.authorize_payment(int(lease_id), float(amount), float(auto_debit))
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
