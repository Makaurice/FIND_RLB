from rest_framework import serializers

class TenantSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    preferred_location = serializers.CharField()
    budget = serializers.IntegerField()
    history = serializers.CharField()
    property_type = serializers.CharField()
    savings = serializers.IntegerField()
    reviews = serializers.ListField(child=serializers.CharField())
