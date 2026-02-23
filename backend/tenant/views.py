from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TenantSerializer
from accounts.permissions import IsTenant

# Placeholder for AI agent integration
# Note: AI agents are located in /ai directory, will be integrated via API calls
# from ai.tenant_agent import TenantAIAgent

class TenantList(APIView):
    permission_classes = [IsAuthenticated, IsTenant]

    def get(self, request):
        tenants = [
            {
                'id': 1,
                'name': 'Alice',
                'preferred_location': 'Downtown',
                'budget': 1500,
                'history': '2 years in city',
                'property_type': 'Apartment',
                'savings': 5000,
                'reviews': ['Great tenant', 'Pays on time']
            }
        ]
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            # AI agent logic will be integrated via API calls
            return Response({'tenant': serializer.data}, status=201)
        return Response(serializer.errors, status=400)
