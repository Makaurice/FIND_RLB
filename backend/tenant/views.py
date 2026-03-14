from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.permissions import IsTenant
from tenant.models import TenantProfile, Lease, Payment
from tenant.serializers import TenantProfileSerializer, LeaseSerializer, PaymentSerializer


class TenantProfileView(APIView):
    """Read/update the currently authenticated tenant's profile."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        profile, _created = TenantProfile.objects.get_or_create(user=request.user)
        serializer = TenantProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile, _created = TenantProfile.objects.get_or_create(user=request.user)
        serializer = TenantProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaseListCreateView(APIView):
    """Create and list leases for the current tenant."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        leases = Lease.objects.filter(tenant=request.user)
        serializer = LeaseSerializer(leases, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {**request.data, 'tenant': request.user.id}
        serializer = LeaseSerializer(data=data)
        if serializer.is_valid():
            lease = serializer.save()
            return Response(LeaseSerializer(lease).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListCreateView(APIView):
    """Create and list payments for the current tenant."""

    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        payments = Payment.objects.filter(lease__tenant=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
