from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    PropertyListingSerializer,
    PricingSettingsSerializer,
    PaymentScheduleSerializer,
    RentHistorySerializer,
    AnalyticsSerializer
)
from accounts.permissions import IsLandlord

class PropertyListingsAPI(APIView):
    permission_classes = [IsAuthenticated, IsLandlord]

    def get(self, request):
        properties = [
            {'id': 1, 'address': '123 Main St', 'property_type': 'Apt', 'status': 'For Rent', 'price': 1200},
            {'id': 2, 'address': '456 Oak Ave', 'property_type': 'House', 'status': 'For Sale', 'price': 250000},
        ]
        serializer = PropertyListingSerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertyListingSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PricingSettingsAPI(APIView):
    permission_classes = [IsAuthenticated, IsLandlord]

    def get(self, request):
        pricing = {
            'monthly_rent': 1200,
            'security_deposit': 2400,
            'lease_term_months': 12,
            'late_fees_percentage': 5.0
        }
        serializer = PricingSettingsSerializer(pricing)
        return Response(serializer.data)

    def post(self, request):
        serializer = PricingSettingsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PaymentScheduleAPI(APIView):
    permission_classes = [IsAuthenticated, IsLandlord]

    def get(self, request):
        schedules = [
            {'id': 1, 'property': '123 Main St', 'due_day': 1, 'amount': 1200, 'frequency': 'Monthly'},
            {'id': 2, 'property': '456 Oak Ave', 'due_day': 15, 'amount': 250000, 'frequency': 'Annual'},
        ]
        serializer = PaymentScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentScheduleSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RentHistoryAPI(APIView):
    permission_classes = [IsAuthenticated, IsLandlord]

    def get(self, request):
        history = [
            {'id': 1, 'property': '123 Main St', 'tenant': 'John Doe', 'amount': 1200, 'date': '2026-02-01', 'status': 'Paid'},
            {'id': 2, 'property': '123 Main St', 'tenant': 'John Doe', 'amount': 1200, 'date': '2026-01-01', 'status': 'Paid'},
            {'id': 3, 'property': '456 Oak Ave', 'tenant': 'Jane Smith', 'amount': 1500, 'date': '2026-02-15', 'status': 'Pending'},
        ]
        serializer = RentHistorySerializer(history, many=True)
        return Response(serializer.data)

class AnalyticsAPI(APIView):
    permission_classes = [IsAuthenticated, IsLandlord]

    def get(self, request):
        analytics = {
            'average_rent': 1350,
            'occupancy_rate': 94.0,
            'price_recommendation': 1250,
            'vacancy_risk': 'Low'
        }
        serializer = AnalyticsSerializer(analytics)
        return Response(serializer.data)

