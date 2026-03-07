from django.contrib import admin

from service.models import UserEvent


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'property', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('user__username', 'metadata')
