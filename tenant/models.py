from django.conf import settings
from django.db import models


class TenantProfile(models.Model):
    """Tenant profile and preference data for recommendations and scoring."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_profile',
    )
    budget_min = models.IntegerField(default=0)
    budget_max = models.IntegerField(default=0)
    preferred_locations = models.JSONField(default=list, blank=True)
    preferred_beds = models.IntegerField(null=True, blank=True)
    preferred_baths = models.IntegerField(null=True, blank=True)
    preferred_amenities = models.JSONField(default=list, blank=True)
    income_monthly = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenant_profile'

    def __str__(self):
        return f"TenantProfile(user={self.user_id})"


class Lease(models.Model):
    """A lease agreement between a tenant and a landlord for a property."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]

    property = models.ForeignKey(
        'property.Property',
        on_delete=models.CASCADE,
        related_name='leases',
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leases',
    )
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='landlord_leases',
    )
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lease'

    def __str__(self):
        return f"Lease(property={self.property_id}, tenant={self.tenant_id}, status={self.status})"


class Payment(models.Model):
    """Rent payment records tied to a lease."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('late', 'Late'),
        ('failed', 'Failed'),
    ]

    lease = models.ForeignKey(
        Lease,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment(lease={self.lease_id}, amount={self.amount}, status={self.status})"


class Review(models.Model):
    """Ratings and reviews between users (tenant <-> landlord)."""

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_written',
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received',
    )
    rating = models.FloatField()
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    helpful = models.IntegerField(default=0)
    unhelpful = models.IntegerField(default=0)

    class Meta:
        db_table = 'review'
        ordering = ['-created_at']

    def __str__(self):
        return f"Review(from={self.reviewer_id}, to={self.target_user_id}, rating={self.rating})"


class TenantTrustScore(models.Model):
    """Persist tenant trust score computations and on-chain verification"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trust_scores',
    )
    payment_consistency = models.FloatField(help_text='0-100', default=0.0)
    lease_completion_rate = models.FloatField(help_text='0-100', default=0.0)
    reviews_score = models.FloatField(help_text='0-100', default=0.0)
    overall_score = models.FloatField(help_text='0-100', default=0.0)
    score_hash = models.CharField(max_length=128, blank=True, default='')
    hedera_tx = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenant_trust_score'
        ordering = ['-updated_at']

    def __str__(self):
        return f"TrustScore(user={self.user_id}, score={self.overall_score})"
