from django.conf import settings
from django.db import models

from property.models import Property


class UserEvent(models.Model):
    """Record user actions to drive analytics and recommendations."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The user who performed the action (if known).",
    )
    event_type = models.CharField(max_length=100, help_text="Type of user event, e.g., 'property_search' or 'view_property'.")
    property = models.ForeignKey(
        Property,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Related property (if applicable).",
    )
    metadata = models.JSONField(default=dict, blank=True, help_text="Optional free-form metadata about the event.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'service'
        ordering = ['-created_at']

    def __str__(self):
        return f"UserEvent(user={self.user}, type={self.event_type}, created_at={self.created_at})"
