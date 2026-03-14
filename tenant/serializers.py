from rest_framework import serializers

from tenant.models import TenantProfile, Lease, Payment, Review


class TenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = [
            'user',
            'budget_min',
            'budget_max',
            'preferred_locations',
            'preferred_beds',
            'preferred_baths',
            'preferred_amenities',
            'income_monthly',
            'created_at',
            'updated_at',
        ]


class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = [
            'id',
            'property',
            'tenant',
            'landlord',
            'start_date',
            'end_date',
            'monthly_rent',
            'status',
            'created_at',
            'updated_at',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'lease',
            'amount',
            'due_date',
            'paid_date',
            'status',
            'method',
            'created_at',
            'updated_at',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'reviewer',
            'target_user',
            'rating',
            'comment',
            'helpful',
            'unhelpful',
            'created_at',
        ]
