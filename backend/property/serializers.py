from rest_framework import serializers

class PropertySerializer(serializers.Serializer):
    propertyId = serializers.IntegerField()
    owner = serializers.CharField()
    location = serializers.CharField()
    metadataURI = serializers.CharField()
    forRent = serializers.BooleanField()
    forSale = serializers.BooleanField()
    price = serializers.IntegerField()
