from rest_framework import serializers

class PropertyListingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    address = serializers.CharField()
    property_type = serializers.CharField()
    status = serializers.CharField()
    price = serializers.IntegerField()

class PricingSettingsSerializer(serializers.Serializer):
    monthly_rent = serializers.IntegerField()
    security_deposit = serializers.IntegerField()
    lease_term_months = serializers.IntegerField()
    late_fees_percentage = serializers.FloatField()

class PaymentScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    property = serializers.CharField()
    due_day = serializers.IntegerField()
    amount = serializers.IntegerField()
    frequency = serializers.CharField()

class RentHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    property = serializers.CharField()
    tenant = serializers.CharField()
    amount = serializers.IntegerField()
    date = serializers.CharField()
    status = serializers.CharField()

class AnalyticsSerializer(serializers.Serializer):
    average_rent = serializers.IntegerField()
    occupancy_rate = serializers.FloatField()
    price_recommendation = serializers.IntegerField()
    vacancy_risk = serializers.CharField()
