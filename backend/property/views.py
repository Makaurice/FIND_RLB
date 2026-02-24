from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PropertySerializer


class PropertyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from property.models import Property
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request):
        from property.models import Property
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            prop = Property.objects.create(
                owner=serializer.validated_data.get('owner', ''),
                location=serializer.validated_data.get('location', ''),
                metadataURI=serializer.validated_data.get('metadataURI', ''),
                forRent=serializer.validated_data.get('forRent', True),
                forSale=serializer.validated_data.get('forSale', False),
                price=serializer.validated_data.get('price', 0)
            )
            return Response(PropertySerializer(prop).data, status=201)
        return Response(serializer.errors, status=400)
