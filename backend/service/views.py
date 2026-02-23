from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    MoverServiceSerializer,
    MovingBookingSerializer,
    MaintenanceRequestSerializer,
    StorageUnitSerializer,
    InventoryItemSerializer
)
from accounts.permissions import IsServiceProvider

class MoversServicesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        services = [
            {'id': 1, 'name': 'Quick Movers Co.', 'rating': 4.8, 'price': 500, 'availability': 'Available', 'reviews': 245},
            {'id': 2, 'name': 'Professional Relocations', 'rating': 4.6, 'price': 600, 'availability': 'Available', 'reviews': 189},
            {'id': 3, 'name': 'Local Moving Experts', 'rating': 4.9, 'price': 450, 'availability': 'Booked', 'reviews': 312},
        ]
        serializer = MoverServiceSerializer(services, many=True)
        return Response(serializer.data)

class MovingBookingsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = [
            {'id': 1, 'provider': 'Quick Movers Co.', 'date': '2026-03-15', 'status': 'Scheduled', 'amount': 500},
            {'id': 2, 'provider': 'Professional Relocations', 'date': '2026-02-20', 'status': 'Completed', 'amount': 600},
        ]
        serializer = MovingBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovingBookingSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MaintenanceRequestsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = [
            {'id': 1, 'issue': 'Leaky faucet', 'priority': 'Medium', 'status': 'In Progress', 'date': '2026-02-18', 'provider': 'Home Fix Pro'},
            {'id': 2, 'issue': 'Broken window latch', 'priority': 'High', 'status': 'Scheduled', 'date': '2026-02-20', 'provider': 'QuickRepairs'},
            {'id': 3, 'issue': 'Paint touch-up', 'priority': 'Low', 'status': 'Completed', 'date': '2026-02-10', 'provider': 'Professional Paint'},
        ]
        serializer = MaintenanceRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaintenanceRequestSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class StorageUnitsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        units = [
            {'id': 1, 'name': 'Downtown Storage Hub', 'size': '100 sq ft', 'price': 150, 'occupancy': 85, 'climate': True, 'security': '24/7'},
            {'id': 2, 'name': 'Suburban Warehouse', 'size': '200 sq ft', 'price': 250, 'occupancy': 60, 'climate': True, 'security': '24/7'},
            {'id': 3, 'name': 'Economy Storage', 'size': '50 sq ft', 'price': 75, 'occupancy': 95, 'climate': False, 'security': 'Business hours'},
        ]
        serializer = StorageUnitSerializer(units, many=True)
        return Response(serializer.data)

class InventoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        inventory = [
            {'id': 1, 'item': 'Furniture', 'quantity': 5, 'location': 'Downtown Storage Hub', 'status': 'Stored'},
            {'id': 2, 'item': 'Boxes (Electronics)', 'quantity': 12, 'location': 'Suburban Warehouse', 'status': 'Stored'},
            {'id': 3, 'item': 'Seasonal Items', 'quantity': 3, 'location': 'Downtown Storage Hub', 'status': 'In Transit'},
        ]
        serializer = InventoryItemSerializer(inventory, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

