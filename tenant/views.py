from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.permissions import IsTenant
from service.events import log_user_event
from tenant.models import TenantProfile, Lease, Payment, Review
from tenant.serializers import (
    TenantProfileSerializer,
    LeaseSerializer,
    PaymentSerializer,
    ReviewSerializer,
)


class TenantProfileAPIView(APIView):
    """Manage tenant profile/preferences."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        profile, _ = TenantProfile.objects.get_or_create(user=request.user)
        return Response(TenantProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = TenantProfile.objects.get_or_create(user=request.user)
        serializer = TenantProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaseListCreateAPIView(APIView):
    """List leases for the current tenant and allow creating new leases."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        leases = Lease.objects.filter(tenant=request.user)
        return Response(LeaseSerializer(leases, many=True).data)

    def post(self, request):
        data = {**request.data, 'tenant': request.user.id}
        serializer = LeaseSerializer(data=data)
        if serializer.is_valid():
            lease = serializer.save()
            log_user_event(
                request.user,
                event_type='lease_created',
                metadata={
                    'lease_id': lease.id,
                    'property_id': lease.property_id,
                    'monthly_rent': float(lease.monthly_rent),
                    'start_date': lease.start_date.isoformat(),
                    'end_date': lease.end_date.isoformat(),
                },
            )
            return Response(LeaseSerializer(lease).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListCreateAPIView(APIView):
    """List tenant payments and create new payment records."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        payments = Payment.objects.filter(lease__tenant=request.user)
        return Response(PaymentSerializer(payments, many=True).data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            log_user_event(
                request.user,
                event_type='rent_payment',
                metadata={
                    'payment_id': payment.id,
                    'lease_id': payment.lease_id,
                    'amount': float(payment.amount),
                    'status': payment.status,
                    'paid_date': payment.paid_date.isoformat() if payment.paid_date else None,
                    'due_date': payment.due_date.isoformat(),
                },
            )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateAPIView(APIView):
    """Create reviews and list reviews received by the current user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Review.objects.filter(target_user=request.user)
        return Response(ReviewSerializer(reviews, many=True).data)

    def post(self, request):
        data = {**request.data, 'reviewer': request.user.id}
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            review = serializer.save()
            log_user_event(
                request.user,
                event_type='review_submitted',
                metadata={
                    'review_id': review.id,
                    'target_user_id': review.target_user_id,
                    'rating': float(review.rating),
                    'comment': review.comment,
                },
            )
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TenantTrustScoreAPIView(APIView):
    """Compute/return tenant trust score (and optionally sync it on-chain)."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        from tenant.trust_score import get_or_create_trust_score

        sync = request.query_params.get('sync_on_chain', 'false').lower() in ['1', 'true', 'yes']
        score = get_or_create_trust_score(request.user.id, sync_on_chain=sync)
        return Response({
            'user': request.user.id,
            'overall_score': score.overall_score,
            'payment_consistency': score.payment_consistency,
            'lease_completion_rate': score.lease_completion_rate,
            'reviews_score': score.reviews_score,
            'score_hash': score.score_hash,
            'hedera_tx': score.hedera_tx,
            'updated_at': score.updated_at,
        })
