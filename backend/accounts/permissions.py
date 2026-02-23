from rest_framework.permissions import BasePermission, IsAuthenticated

class IsTenant(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'tenant'

class IsLandlord(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'landlord'

class IsServiceProvider(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'service_provider'

class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'admin'

class IsRoleOrReadOnly(IsAuthenticated):
    """
    Allow full access to users with specific roles, read-only for others.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role in self.allowed_roles

class IsLandlordOrReadOnly(IsRoleOrReadOnly):
    allowed_roles = ['landlord', 'admin']

class IsServiceProviderOrReadOnly(IsRoleOrReadOnly):
    allowed_roles = ['service_provider', 'admin']

class IsTenantOrReadOnly(IsRoleOrReadOnly):
    allowed_roles = ['tenant', 'admin']
