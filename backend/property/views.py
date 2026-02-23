from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PropertySerializer


class PropertyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example: fetch properties from smart contract (placeholder)
        properties = [
            {
                'propertyId': 1,
                'owner': '0x123...',
                'location': 'Downtown',
                'metadataURI': 'ipfs://abc',
                'forRent': True,
                'forSale': False,
                'price': 1200
            }
        ]
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Example: register property via smart contract (placeholder)
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            # Call smart contract function here
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
