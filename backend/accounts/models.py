from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = [
    ('tenant', 'Tenant'),
    ('landlord', 'Landlord'),
    ('service_provider', 'Service Provider'),
    ('admin', 'Admin'),
]

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='tenant')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
