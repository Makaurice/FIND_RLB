from rest_framework import serializers

class MoverServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    rating = serializers.FloatField()
    price = serializers.IntegerField()
    availability = serializers.CharField()
    reviews = serializers.IntegerField()

class MovingBookingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    provider = serializers.CharField()
    date = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.IntegerField()

class MaintenanceRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    issue = serializers.CharField()
    priority = serializers.CharField()
    status = serializers.CharField()
    date = serializers.CharField()
    provider = serializers.CharField()

class StorageUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    size = serializers.CharField()
    price = serializers.IntegerField()
    occupancy = serializers.IntegerField()
    climate = serializers.BooleanField()
    security = serializers.CharField()

class InventoryItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    item = serializers.CharField()
    quantity = serializers.IntegerField()
    location = serializers.CharField()
    status = serializers.CharField()
