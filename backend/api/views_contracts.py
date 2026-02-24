class RentalHistoryView(APIView):
    """API endpoint to get rental/payment history for a landlord or tenant."""
    def get(self, request):
        # In a real system, fetch from DB or contracts. Here, return sample history.
        sample_history = [
            {
                'id': 1,
                'property': '123 Main St',
                'tenant': 'John Doe',
                'amount': 1200,
                'date': '2026-02-01',
                'status': 'Paid',
            },
            {
                'id': 2,
                'property': '123 Main St',
                'tenant': 'John Doe',
                'amount': 1200,
                'date': '2026-01-01',
                'status': 'Paid',
            },
            {
                'id': 3,
                'property': '456 Oak Ave',
                'tenant': 'Jane Smith',
                'amount': 1500,
                'date': '2026-02-15',
                'status': 'Pending',
            },
        ]
        return Response({'history': sample_history}, status=status.HTTP_200_OK)
from datetime import datetime, timedelta

class TenantEventsView(APIView):
    """API endpoint to get reminders/events for a tenant (rent due, lease renewal, maintenance, etc.)"""
    def get(self, request):
        # In a real system, fetch from DB or contracts. Here, return sample events.
        sample_events = [
            {
                'id': 1,
                'title': 'Rent Payment Due',
                'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                'type': 'payment',
                'time': '00:00',
            },
            {
                'id': 2,
                'title': 'Lease Renewal Notice',
                'date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'type': 'lease',
                'time': '09:00',
            },
            {
                'id': 3,
                'title': 'Maintenance Scheduled',
                'date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                'type': 'maintenance',
                'time': '14:00',
            },
        ]
        return Response({'events': sample_events}, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .contracts import get_contract

class RegisterPropertyView(APIView):
    """Register a property as an NFT. In production, integrates with PropertyNFT contract on Hedera."""
    def post(self, request):
        data = request.data
        try:
            location = data.get('location')
            metadata_uri = data.get('metadata_uri')
            price = data.get('price', 0)
            beds = data.get('beds', 0)
            baths = data.get('baths', 0)
            sqft = data.get('sqft', 0)
            
            # Validate required fields
            if not location or price <= 0:
                return Response({'error': 'Location and price required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call Hedera PropertyNFT contract
            # contract = get_contract('PropertyNFT')
            # tx = contract.functions.registerProperty(location, metadata_uri, price, beds, baths, sqft, []).send()
            
            # For now: Log and return success with transaction hash simulation
            transaction_data = {
                'propertyId': 1,  # Would come from contract
                'owner': request.user.username if hasattr(request, 'user') else 'anonymous',
                'location': location,
                'price': price,
                'status': 'AVAILABLE',
                'transactionHash': '0x' + 'a' * 64,
                'timestamp': str(datetime.now()),
            }
            return Response(transaction_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateLeaseView(APIView):
    """Create a lease agreement on-chain. Links tenant, landlord, property, and terms."""
    def post(self, request):
        data = request.data
        try:
            property_id = data.get('property_id')
            tenant = data.get('tenant')
            monthly_rent = data.get('monthly_rent')
            security_deposit = data.get('security_deposit', 0)
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            if not all([property_id, tenant, monthly_rent, start_date, end_date]):
                return Response({'error': 'All lease fields required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call Hedera LeaseAgreement contract
            # contract = get_contract('LeaseAgreement')
            # tx = contract.functions.createLease(property_id, tenant, monthly_rent, security_deposit, start_date, end_date).send()
            
            lease_data = {
                'leaseId': 1,
                'propertyId': property_id,
                'tenant': tenant,
                'landlord': request.user.username if hasattr(request, 'user') else 'anonymous',
                'monthlyRent': monthly_rent,
                'securityDeposit': security_deposit,
                'startDate': start_date,
                'endDate': end_date,
                'status': 'PENDING',
                'transactionHash': '0x' + 'b' * 64,
            }
            return Response(lease_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PayRentView(APIView):
    """Process rent payment. Pulls from tenant wallet or executes escrow release."""
    def post(self, request, lease_id):
        data = request.data
        try:
            amount = data.get('amount')
            
            if not amount or amount <= 0:
                return Response({'error': 'Valid amount required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call Hedera RentEscrow contract
            # contract = get_contract('RentEscrow')
            # tx = contract.functions.payRent(lease_id, amount).send(transaction={'value': amount})
            
            payment_data = {
                'leaseId': lease_id,
                'amount': amount,
                'paidBy': request.user.username if hasattr(request, 'user') else 'anonymous',
                'status': 'COMPLETED',
                'date': str(datetime.now()),
                'transactionHash': '0x' + 'c' * 64,
            }
            return Response(payment_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DepositSavingsView(APIView):
    """Deposit into savings-to-own plan. Accumulates toward property purchase."""
    def post(self, request, plan_id):
        data = request.data
        try:
            amount = data.get('amount')
            
            if not amount or amount <= 0:
                return Response({'error': 'Valid amount required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call Hedera SavingsVault contract
            # contract = get_contract('SavingsVault')
            # tx = contract.functions.depositSavings(plan_id).send(transaction={'value': amount})
            
            deposit_data = {
                'planId': plan_id,
                'amount': amount,
                'depositedBy': request.user.username if hasattr(request, 'user') else 'anonymous',
                'status': 'CONFIRMED',
                'date': str(datetime.now()),
                'transactionHash': '0x' + 'd' * 64,
            }
            return Response(deposit_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PayOnBehalfView(APIView):
    """Guardian/sponsor pays rent on behalf of tenant. Records on-chain."""
    def post(self, request):
        data = request.data
        try:
            tenant = data.get('tenant')
            lease_id = data.get('lease_id')
            amount = data.get('amount')
            
            if not all([tenant, lease_id, amount]) or amount <= 0:
                return Response({'error': 'All fields required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call Hedera ThirdPartyPayment contract
            # contract = get_contract('ThirdPartyPayment')
            # tx = contract.functions.payOnBehalf(tenant, lease_id, amount).send(transaction={'value': amount})
            
            payment_data = {
                'leaseId': lease_id,
                'tenant': tenant,
                'amount': amount,
                'paidBy': request.user.username if hasattr(request, 'user') else 'anonymous',
                'status': 'COMPLETED',
                'date': str(datetime.now()),
                'transactionHash': '0x' + 'e' * 64,
            }
            return Response(payment_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateReputationView(APIView):
    """Update user reputation score on-chain. Triggered by payment, lease completion, or reviews."""
    def post(self, request, user, action):
        try:
            score = request.data.get('score', 0)
            reason = request.data.get('reason', '')
            
            if score < 0 or score > 100:
                return Response({'error': 'Score must be 0-100'}, status=status.HTTP_400_BAD_REQUEST)
            
            # In production: Call Hedera Reputation contract
            # contract = get_contract('Reputation')
            # Action determines which reputation metric to update
            # if action == 'payment': contract.functions.updatePaymentConsistency(user, score).send()
            # elif action == 'lease': contract.functions.updateLeaseCompletionRate(user, score).send()
            # elif action == 'review': contract.functions.updateReviewsScore(user, score).send()
            
            reputation_data = {
                'user': user,
                'action': action,
                'score': score,
                'reason': reason,
                'status': 'UPDATED',
                'date': str(datetime.now()),
                'transactionHash': '0x' + 'f' * 64,
            }
            return Response(reputation_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
